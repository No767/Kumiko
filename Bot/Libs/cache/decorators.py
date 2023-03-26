import uuid
from functools import wraps
from typing import Any, Callable, Optional

from redis.asyncio.connection import ConnectionPool

from .redis_cache import CommandKeyBuilder, KumikoCache


def cached(
    connection_pool: ConnectionPool,
    command_key: Optional[str],
    ttl: int = 30,
) -> Callable[..., Any]:
    """A decorator to cache the result of a function that returns a `str` to Redis.

    **Note**: The return type of the corountine used has to be `str` or `bytes`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        command_key (Optional[str]): Command key to use
        ttl (int, optional): TTL (Time-To-Live). Defaults to 30.

    Returns:
        Callable[..., Any]: The wrapper function
    """

    def wrapper(func: Callable[..., Any]) -> Any:
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


def cachedJson(
    connection_pool: ConnectionPool,
    command_key: Optional[str],
    ttl: int = 30,
) -> Callable[..., Any]:
    """A decorator to cache the result of a function that returns a `dict` to Redis.

    **Note**: The return type of the corountine used has to be `dict`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        command_key (Optional[str]): Command key to use
        ttl (int, optional): TTL (Time-To-Live). Defaults to 30.

    Returns:
        Callable[..., Any]: The wrapper function
    """

    def wrapper(func: Callable[..., Any]) -> Any:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            currFunc = await func(*args, **kwargs)
            if currFunc is None:
                return None
            cache = KumikoCache(connection_pool=connection_pool)
            key = (
                CommandKeyBuilder(id=uuid.uuid4(), command=cachedJson.__name__)
                if command_key is None
                else command_key
            )
            if await cache.cacheExists(key=key) is False:
                await cache.setJSONCache(key=key, value=currFunc, ttl=ttl)
            else:
                return await cache.getJSONCache(key=key)
            return currFunc

        return wrapped

    return wrapper
