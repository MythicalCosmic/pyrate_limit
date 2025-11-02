from __future__ import annotations
from functools import partial
from typing import Callable, overload, Any
from .core import RateLimiter

@overload
def ratelimit(calls: int, per: int) -> Callable[[Callable], Callable]: ...
@overload
def ratelimit(calls: int, per: int, *, storage: Any) -> Callable[[Callable], Callable]: ...

def ratelimit(calls: int, per: int, storage=None, key_prefix: str = "ratelimit") -> Callable[[Callable], Callable]:
    limiter = RateLimiter(calls, per, storage, key_prefix)
    return limiter