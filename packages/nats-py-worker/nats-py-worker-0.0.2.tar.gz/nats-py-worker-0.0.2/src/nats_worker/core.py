import asyncio
import contextlib
import functools
import inspect
import logging
import os
import signal
from collections.abc import AsyncIterator
from typing import (
    AsyncIterable,
    Optional,
    Protocol,
    Tuple,
    Union,
)

from nats import connect as nats_connect
from nats.aio.client import Client as NatsClient
from nats.errors import (
    MsgAlreadyAckdError,
    TimeoutError as NatsTimeoutError,
)
from nats.js.api import ConsumerConfig, DeliverPolicy, KeyValueConfig
from nats.js.errors import (
    KeyDeletedError as NatsKeyDeletedError,
    KeyNotFoundError as NatsKeyNotFoundError,
    KeyWrongLastSequenceError as NatsKeyWrongLastSequenceError,
)
from nats.js.kv import KeyValue as NatsKeyValue


logger = logging.getLogger(__name__)


class WorkerTaskProtocol(Protocol):
    async def __call__(self, *, connection: NatsClient):
        pass


class Worker:
    def __init__(
        self,
        name,
        servers=None,
        servers_default="nats://localhost:4222",
    ):
        """
        Initializes a new worker.

        :param name:
        The name of the worker. This is used as a prefix for subscriptions to
        prevent collisions with workers in other applications.
        :param servers:
        A comma-separated list of servers to connect to.
        Defaults to the value of the `NATS_SERVERS` environment variable, or
        `nats://localhost:4222` if the environment variable is not set.
        :param servers_default:
        The default value for the `servers` parameter.
        """
        self.name = name
        self.servers = servers or os.environ.get(
            "NATS_SERVERS", servers_default
        )
        self.ready = asyncio.Event()
        self.abort = asyncio.Event()
        self.closed = asyncio.Event()
        self.connection: Optional[NatsClient] = None
        self.queue = asyncio.Queue()
        self.sentinel = object()

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[NatsClient]:
        await self.ready.wait()
        yield self.connection

    async def start(self, init=None):
        """
        Starts the worker and waits until it has shut down.

        :param init:
        An optional coroutine to run when the worker starts, before the
        connection is made available to the application.
        """

        logger.debug(f"Starting worker {self.name}")

        try:
            async with await nats_connect(
                servers=self.servers.split(","),
                max_reconnect_attempts=-1,
            ) as connection:
                if init is not None:
                    await init(connection=connection)
                self.connection = connection
                self.ready.set()
                loop = asyncio.get_running_loop()
                tasks = []

                exceptions = []

                def task_done(task):
                    try:
                        ex = task.exception()
                    except asyncio.CancelledError:
                        ex = None
                    if ex:
                        self.queue.put_nowait(self.sentinel)
                        exceptions.append(ex)

                while True:
                    f = await self.queue.get()
                    if f is self.sentinel:
                        break
                    task = loop.create_task(f(connection=connection))
                    task.add_done_callback(task_done)
                    tasks.append(task)
                    # Clean up completed tasks to prevent memory leaks.
                    for task in tasks:
                        if task.done():
                            tasks.remove(task)
                for task in tasks:
                    try:
                        task.cancel(f"Worker {self.name} is shutting down")
                    except asyncio.CancelledError:
                        pass
                for task in tasks:
                    try:
                        await task
                    except BaseException as ex:
                        exceptions.append(ex)
                for ex in exceptions:
                    # In Python 3.11 we could raise an exception group here.
                    # For now, we'll just try to raise the first exception we
                    # encountered, assuming that it's the root cause.
                    raise ex
        finally:
            self.closed.set()

    async def start_as_task(self, init=None):
        coro = self.start(init=init)
        return asyncio.create_task(coro)

    def start_as_future(self, init=None):
        loop = asyncio.get_event_loop()
        coro = self.start(init=init)
        return asyncio.run_coroutine_threadsafe(coro, loop=loop)

    def start_as_app(self, init=None):
        loop = asyncio.new_event_loop()

        def cancel():
            nonlocal future
            future.cancel()

        loop.add_signal_handler(signal.SIGINT, cancel)
        loop.add_signal_handler(signal.SIGTERM, cancel)

        def exception_handler(loop, context):
            loop.default_exception_handler(context)
            cancel()

        loop.set_exception_handler(exception_handler)

        future = asyncio.run_coroutine_threadsafe(
            self.start(init=init), loop=loop
        )
        return loop.run_until_complete(asyncio.wrap_future(future, loop=loop))

    async def stop(self):
        """
        Stops the worker.

        Waits until the connection is closed.

        Background tasks will be cancelled, and any exceptions raised by them
        will be propagated from the call to start().
        """
        self.queue.put_nowait(self.sentinel)
        await self.closed.wait()

    async def stop_as_task(self):
        await asyncio.create_task(self.stop())

    def stop_as_future(self):
        loop = asyncio.get_event_loop()
        return asyncio.run_coroutine_threadsafe(self.stop(), loop=loop)

    def schedule(self, f: WorkerTaskProtocol):
        """
        Schedules a function to run in the background, using the worker's event
        loop.

        :param f: The function to run.
        """

        self.queue.put_nowait(f)

    async def tail(self, *, subject, ack_wait=None):
        async with self.connect() as connection:
            async for batch in tail(
                connection=connection,
                subject=subject,
                ack_wait=ack_wait,
            ):
                yield batch

    async def consume(self, *, name, subject, batch_size=1, ack_wait=None):
        name = f"{self.name}_{name}"
        async with self.connect() as connection:
            async for batch in consume(
                connection=connection,
                name=name,
                subject=subject,
                batch_size=batch_size,
                ack_wait=ack_wait,
            ):
                yield batch

    async def scan(self, *, subject, ordered=False):
        async with self.connect() as connection:
            async for msg in scan(
                connection=connection, subject=subject, ordered=ordered
            ):
                yield msg

    async def publish_msgs(
        self,
        msgs: AsyncIterable[bytes],
        *,
        subject,
        headers: Optional[dict] = None,
    ):
        async with self.connect() as connection:
            await publish_msgs(
                connection=connection,
                subject=subject,
                msgs=msgs,
                headers=headers,
            )

    async def publish_msg(
        self, msg: bytes, *, subject, headers: Optional[dict] = None
    ):
        async with self.connect() as connection:
            await publish_msg(
                connection=connection,
                subject=subject,
                msg=msg,
                headers=headers,
            )

    async def create_bucket(self, *, bucket: str):
        async with self.connect() as connection:
            await create_bucket(connection=connection, bucket=bucket)

    async def save_value(
        self, *, key: str, value: bytes, bucket: str, last=None
    ) -> bool:
        async with self.connect() as connection:
            return await save_value(
                connection=connection,
                key=key,
                value=value,
                bucket=bucket,
                last=last,
            )

    KeyValueOptionalRevision = Union[Tuple[str, bytes], Tuple[str, bytes, int]]

    async def save_values(
        self,
        *,
        values: AsyncIterable[KeyValueOptionalRevision],
        bucket: str,
    ):
        async with self.connect() as connection:
            await save_values(
                connection=connection, values=values, bucket=bucket
            )

    async def get_value(self, *, key: str, bucket: str) -> NatsKeyValue.Entry:
        async with self.connect() as connection:
            return await get_value(
                connection=connection, key=key, bucket=bucket
            )

    async def watch_values(self, *, key: str, bucket: str):
        async with self.connect() as connection:
            async for entry in watch_values(
                connection=connection, key=key, bucket=bucket
            ):
                yield entry

    async def list_values(self, *, key: str, bucket: str):
        async with self.connect() as connection:
            async for entry in list_values(
                connection=connection, key=key, bucket=bucket
            ):
                yield entry

    def background(self):
        def decorator(f):
            self.schedule(f)
            return f

        return decorator

    def background_consumer(
        self, *, name=None, subject, batch_size=1, ack_wait=None
    ):
        """
        Registers a function to run as durable consumer in the background.

        Background consumers are started when the worker starts, and stopped
        when the worker stops.

        Unhandled exceptions from background consumers will shut down the
        worker and all other background tasks.

        If multiple consumers have the same name, they will balance the load
        between them, even if they are running on different machines. To
        prevent accidental collisions, consumer names are prefixed with the
        worker's name.

        :param name:
        The name of the consumer. Will be prefixed with the worker's name. Uses
        a name derived from the function name if not provided.
        :param subject:
        The name of the subject (or subject pattern) to consume.
        :param batch_size:
        The number of messages to consume at a time. If the batch size is 1,
        then the function will be called with a single message at a time,
        otherwise the function will be called with a list of messages.
        :param ack_wait:
        The amount of time to wait for an ack before resending a message. You
        can also extend the timer for each message by calling in_progress().
        :return:
        A decorator that registers functions to run as a durable consumer.
        """

        def decorator(f):
            nonlocal name
            if name is None:
                name = f.__name__

            name = f"{self.name}_{name}"

            @functools.wraps(f)
            async def apply(*, connection: NatsClient):
                kwargs = {}
                inject_into_kwargs(
                    f,
                    kwargs,
                    worker=self,
                    name=name,
                    subject=subject,
                    batch_size=batch_size,
                    ack_wait=ack_wait,
                )
                async for batch in consume(
                    connection=connection,
                    name=name,
                    subject=subject,
                    batch_size=batch_size,
                    ack_wait=ack_wait,
                ):
                    await f(batch, **kwargs)

            self.schedule(apply)

            return f

        return decorator

    def background_state_machine(
        self, *, name=None, subject, bucket=None, key_map=None, ack_wait=None
    ):
        """
        Registers a function to run as durable state machine in the background.
        The function will be given the current state and an event from the
        subject. It should either return a new state value, or None if no
        change is required.

        Background state machines are started when the worker starts, and
        stopped when the worker stops.

        Unhandled exceptions from background state machines will shut down the
        worker and all other background tasks.

        To avoid processing events out-of-order, state machines use consumers
        with max_ack_pending set to 1. This means that only one instance can be
        running at a time. To increase throughput, you can run multiple
        instances using NATS' deterministic subject token partitioning to
        distribute events to a fixed number of consumers listening for their
        own dedicated subjects.

        :param name:
        The name of the state machine. Will be prefixed with the worker's name.
        Uses a name derived from the function name if not provided.
        :param subject:
        The name of the subject (or subject pattern) to consume for events.
        :param subject:
        The name of the bucket to read and store state from.
        :param key_map:
        A function that maps events to keys in the bucket. If not provided, the
        event subject is used as the key.
        :param ack_wait:
        The amount of time to wait for an ack before resending a message. You
        can also extend the timer for each message by calling in_progress().
        :return:
        A decorator that registers functions to run as a state machine.
        """

        # TODO: Contribute a change to NATS to enable MaxAcksPendingPerSubject
        #       so that we can run several of these consumers in parallel
        #       threads.
        #       https://github.com/nats-io/nats-server/issues/4273

        if key_map is None:

            def subject_as_key(msg):
                return msg.subject

            key_map = subject_as_key

        def decorator(f):
            nonlocal name
            if name is None:
                name = f.__name__

            name = f"{self.name}_{name}"

            @functools.wraps(f)
            async def apply(*, connection: NatsClient):
                kwargs = {}
                inject_into_kwargs(
                    f,
                    kwargs,
                    worker=self,
                    name=name,
                    subject=subject,
                    bucket=bucket,
                    ack_wait=ack_wait,
                )

                async for msg in consume(
                    connection=connection,
                    name=name,
                    subject=subject,
                    batch_size=1,
                    ack_wait=ack_wait,
                    max_ack_pending=1,
                ):
                    key = key_map(msg)
                    state_entry = await get_value(
                        connection=connection, bucket=bucket, key=key
                    )
                    new_state = await f(state_entry, msg, **kwargs)
                    if new_state is not None:
                        await save_value(
                            connection=connection,
                            bucket=bucket,
                            key=key,
                            value=new_state,
                            last=state_entry.revision,
                        )

            self.schedule(apply)

            return f

        return decorator

    async def delete_value(self, bucket, key):
        async with self.connect() as connection:
            return await delete_value(
                connection=connection, bucket=bucket, key=key
            )

    async def purge_stream(self, subject):
        async with self.connect() as connection:
            return await purge_stream(connection=connection, subject=subject)


async def consume(
    *,
    connection: NatsClient,
    name,
    subject,
    batch_size=1,
    ack_wait=None,
    max_ack_pending=None,
):
    config = ConsumerConfig(ack_wait=ack_wait, max_ack_pending=max_ack_pending)
    sub = await connection.jetstream().pull_subscribe(
        durable=name, subject=subject, config=config
    )
    while True:
        try:
            batch = await sub.fetch(batch=batch_size)
        except NatsTimeoutError:
            continue
        try:
            yield batch if batch_size != 1 else batch[0]
            for msg in batch:
                try:
                    await msg.ack()
                except MsgAlreadyAckdError:
                    pass
        finally:
            for msg in batch:
                try:
                    await msg.nak()
                except MsgAlreadyAckdError:
                    pass


async def tail(*, connection: NatsClient, subject, ack_wait):
    config = ConsumerConfig(
        ack_wait=ack_wait, deliver_policy=DeliverPolicy.NEW
    )
    sub = await connection.jetstream().subscribe(
        subject=subject, config=config, manual_ack=True
    )
    while True:
        try:
            msg = await sub.next_msg()
        except NatsTimeoutError:
            continue
        try:
            yield msg
            await msg.ack()
        finally:
            try:
                await msg.nak()
            except MsgAlreadyAckdError:
                pass


async def scan(*, connection: NatsClient, subject, ordered):
    sub = await connection.jetstream().subscribe(
        subject=subject, ordered_consumer=ordered
    )
    try:
        while True:
            try:
                msg = await sub.next_msg()
            except NatsTimeoutError:
                break
            yield msg
    finally:
        await sub.unsubscribe()


async def publish_msgs(
    msgs: AsyncIterable[bytes],
    *,
    connection: NatsClient,
    subject,
    headers: Optional[dict] = None,
):
    async for msg in msgs:
        await connection.jetstream().publish(
            subject=subject, payload=msg, headers=headers
        )


async def publish_msg(
    msg: bytes,
    *,
    connection: NatsClient,
    subject,
    headers: Optional[dict] = None,
):
    await connection.jetstream().publish(
        subject=subject, payload=msg, headers=headers
    )


async def purge_stream(*, connection: NatsClient, subject):
    stream = await connection.jetstream().find_stream_name_by_subject(subject)
    await connection.jetstream().purge_stream(stream, subject=subject)


async def create_bucket(*, connection: NatsClient, bucket: str):
    config = KeyValueConfig(bucket=bucket)
    await connection.jetstream().create_key_value(config=config)


async def save_value(
    *, connection: NatsClient, key: str, value: bytes, bucket: str, last=None
) -> bool:
    store = await connection.jetstream().key_value(bucket=bucket)
    if last is None:
        try:
            await store.create(key=key, value=value)
            return True
        except NatsKeyWrongLastSequenceError:
            return False
    else:
        try:
            await store.update(key=key, value=value, last=last)
            return True
        except NatsKeyWrongLastSequenceError:
            return False


async def save_values(
    *,
    connection: NatsClient,
    values: AsyncIterable[Union[Tuple[str, bytes], Tuple[str, bytes, int]]],
    bucket: str,
):
    store = await connection.jetstream().key_value(bucket=bucket)
    async for tuple in values:
        if len(tuple) == 2:
            key, value = tuple
            last = None
        else:
            key, value, last = tuple

        if last is None:
            try:
                await store.create(key=key, value=value)
            except NatsKeyWrongLastSequenceError:
                pass
        else:
            try:
                await store.update(key=key, value=value, last=last)
            except NatsKeyWrongLastSequenceError:
                pass


async def get_value(
    *, connection: NatsClient, key: str, bucket: str
) -> Optional[NatsKeyValue.Entry]:
    store = await connection.jetstream().key_value(bucket=bucket)
    try:
        return await store.get(key=key)
    except (NatsKeyNotFoundError, NatsKeyDeletedError):
        return None


async def delete_value(*, connection: NatsClient, key: str, bucket: str):
    store = await connection.jetstream().key_value(bucket=bucket)
    try:
        await store.delete(key=key)
    except (NatsKeyNotFoundError, NatsKeyDeletedError):
        pass


async def watch_values(*, connection: NatsClient, key: str, bucket: str):
    store = await connection.jetstream().key_value(bucket=bucket)
    watcher = await store.watch(key)
    while True:
        try:
            entry = await watcher.updates()
        except NatsTimeoutError:
            continue
        if entry is not None:
            yield entry


async def list_values(*, connection: NatsClient, key: str = ">", bucket: str):
    store = await connection.jetstream().key_value(bucket=bucket)
    watcher = await store.watch(key, ignore_deletes=True)
    async for entry in watcher:
        if not entry:
            break
        yield entry
    await watcher.stop()


def inject_into_kwargs(f, kwargs, **injections):
    sig = inspect.signature(f)
    for p in sig.parameters:
        if p in injections:
            kwargs[p] = injections[p]
