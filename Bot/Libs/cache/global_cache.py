import builtins

from .mem_cache import MemoryCache


def setupMemCacheBuiltin() -> None:
    """Setup func to set up the builtins memCache"""
    builtins.memCache: MemoryCache = MemoryCache()  # type: ignore
