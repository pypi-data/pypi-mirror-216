import pytest
import asyncio
from nats_worker import Worker


def test_create_worker():
    try:
        Worker(name="web")
    except Exception as e:
        raise

def test_create_worker_no_name():
    with pytest.raises(TypeError):
        Worker()

@pytest.mark.asyncio
async def test_worker_start_stop():
    name = "web"
    worker = Worker(name=name)
    try:
        await asyncio.wait_for(worker.start(), timeout=2)
    except asyncio.TimeoutError:
        pass
    assert worker.name is name
    await worker.stop()