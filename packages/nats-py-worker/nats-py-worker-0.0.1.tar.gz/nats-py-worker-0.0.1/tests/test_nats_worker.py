import pytest
from nats_worker import Worker


def test_create_worker():
    function_name = test_create_worker.__name__
    try:
        worker = Worker(name="web")
        print(f"{function_name} - PASSED")
    except Exception as e:
        print(f"{function_name} - FAILED: {str(e)}")
        raise

def test_create_worker_no_name():
    functionName = test_create_worker_no_name.__name__
    try:
        with pytest.raises(TypeError) as exc_info:
            worker = Worker()
        assert "missing 1 required positional argument: 'name'" in str(exc_info.value)
        print(f"{functionName} - PASSED")
    except AssertionError:
        print(f"{functionName} - FAILED")
        raise

def test_worker_start():
    worker = Worker(name="web")
    worker.start()
