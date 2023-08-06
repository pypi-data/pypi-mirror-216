# NATS Worker
[![pypi](https://img.shields.io/pypi/v/nats-py-worker.svg)](https://pypi.org/project/nats-py-worker)
[![Versions](https://img.shields.io/pypi/pyversions/nats-py-worker.svg)](https://pypi.org/project/nats-py-worker)
[![License MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit/)

An opinionated utility for using [NATS](https://nats.io) as a worker queue with NATS.py.

# Example

```python
# pip install nats-py-worker

import nats_worker
from nats.js.api import StreamConfig, KeyValueConfig

worker = Worker(name="demo")

async def init_nats(connection):
    connection.jetstream().add_stream(new StreamConfig(name="events", subjects=["inbox.*", "outbox.*"]))
    connection.jetstream().create_key_value(config=KeyValueConfig(bucket="state"))

@worker.background_consumer(subject="inbox.*")
async def watch_incoming(msg):
    ...

@worker.background_state_machine(subject="inbox.*", bucket="state")
async def next_state(kv, msg):
    ...
    await worker.publish_msg(subject=outbox, payload=side_effect)
    ...
    return new_state

if __name__ == '__main__':
    worker.start_as_app()
```

## Supported platforms

Should be compatible with at least [Python +3.7](https://github.com/nats-io/nats.py#supported-platforms).

## Installing

```bash
pip install nats-py-worker
```

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The gitlab-ci.yml is currently setup to push to PyPi when merged to main. Make sure you have updated the version other wise it will fail.

## License

Unless otherwise noted, the NATS Worker source files are distributed under
the MIT license found in the LICENSE file.
