import uuid
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

from redis.asyncio.connection import ConnectionPool

from .redis_cache import CommandKeyBuilder, KumikoCache

T = TypeVar("T")


def cached(
    connection_pool: ConnectionPool,
    command_key: Optional[str],
    ttl: int = 30,
) -> Callable[..., T]:
    """A decorator to cache the result of a function"""

    def wrapper(func: Callable[..., T]) -> Any:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            currFunc = await func(*args, **kwargs)
            cache = KumikoCache(connection_pool=connection_pool)
            key = (
                CommandKeyBuilder(id=uuid.uuid4(), command=cached.__name__)
                if command_key is None
                else command_key
            )
            if await cache.cacheExists(key=key) is False:
                await cache.setBasicCache(key=key, value=currFunc, ttl=ttl)
            else:
                return await cache.getBasicCache(key=key)
            return currFunc

        return wrapped

    return wrapper
