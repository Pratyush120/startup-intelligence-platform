import os
import time
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CacheProvider(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        pass


class MemoryCacheProvider(CacheProvider):
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if not entry:
            return None
            
        if time.time() > entry["expires_at"]:
            del self._store[key]
            return None
            
        return entry["value"]

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        self._store[key] = {
            "value": value,
            "expires_at": time.time() + ttl_seconds
        }

class RedisCacheProvider(CacheProvider):
    def __init__(self):
        # Placeholder for future Redis integration
        self._client = None
        logger.warning("RedisCacheProvider is a stub. Falling back to Memory.")

    def get(self, key: str) -> Optional[Any]:
        return None

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        pass

def get_cache() -> CacheProvider:
    backend = os.getenv("CACHE_BACKEND", "memory").lower()
    if backend == "redis":
        return RedisCacheProvider()
    return MemoryCacheProvider()

# Global singleton cache for the application
global_cache = get_cache()
