from __future__ import annotations
from time import time, sleep
from typing import Callable, Any
from .storage import RateLimitStorage, InMemoryStorage


class RateLimiter:
    def __init__(self, calls: int, per: int, storage: RateLimitStorage | None = None, key_prefix: str = "ratelimit"):
        self.calls = calls
        self.per = per
        self.storage = storage or InMemoryStorage
        self.key_prefix = key_prefix

    def _make_key(self, func: Callable) -> str:
            return f"{self.key_prefix}: {func.__module__}: {func.__qualname__}"
        
    def __call__(self, func: Callable) -> Callable:
        key = self._make_key(func)

        def wrapper(*args, **kwargs) -> Any:
            now = time()
            timestamps = self.storage.cleanup(key, now, self.per)

            if len(timestamps) >= self.calls:
                sleep_time = self.per - (now - timestamps[0])
                if sleep_time > 0:
                    sleep(sleep_time)
                return wrapper(*args, **kwargs)

            self.storage.set(key, timestamps + [time()])
            return func(*args, **kwargs)

        return wrapper