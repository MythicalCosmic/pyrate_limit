import time
from limitless_py import ratelimit, InMemoryStorage

def test_ratelimit_blocks():
    calls = []

    @ratelimit(calls=2, per=1)
    def limited():
        calls.append(time.time())

    limited()
    limited()
    start = time.time()
    limited() 
    elapsed = time.time() - start

    assert len(calls) == 3
    assert elapsed >= 0.9