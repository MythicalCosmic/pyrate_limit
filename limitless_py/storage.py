from __future__ import annotations 
from abc import ABC, abstractmethod
from typing import List, Protocol
from time import time
import threading


class RateLimitStorage(Protocol):
    def get(self, key: str) -> List[float]: ...
    def set(self, key: str, timestaps: List[float]) -> None: ...
    def cleanup(self, key: str, now: float, window: int) -> List[float]: ...

class InMemoryStorage:
    def __init__(self):
        self._data: dict[str, List[float]] = {}
        self.lock = threading.Lock()
        
    def get(self, key: str) -> List[float]:
        with self.lock:
            return self._data.get(key, []).copy()
        
    def set(self, key: str, timestamps: List[float]):
        with self.lock:
            self._data[key] = timestamps
        
    def cleanup(self, key: str, now: float, window: int) -> List[float]:
        timestamps = self.get(key)
        valid = [t for t in timestamps if t > now - window]
        self.set(key, valid)
        return valid