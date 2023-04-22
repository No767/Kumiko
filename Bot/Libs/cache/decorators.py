import uuid
from functools import wraps
from typing import Any, Callable, Union

from redis.asyncio.connection import ConnectionPool

from .redis_cache import CommandKeyBuilder, KumikoCache


class cache:
    """A decorator to cache the result of a function that returns a `str` to Redis.

    **Note**: The return type of the coroutine used has to be `str` or `bytes`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        ttl (int, optional): TTL (Time-To-Live). Defaults to 30.
    """

    def __init__(self, connection_pool: ConnectionPool, ttl: int = 30):
        self.connection_pool = connection_pool
        self.ttl = ttl

    def __call__(self, func: Callable, *args: Any, **kwargs: Any):
        @wraps(func)
        async def wrapper(id: int, *args: Any, **kwargs: Any):
            return await self.deco(func, id, *args, **kwargs)

        return wrapper

    async def deco(self, func: Callable, id: Union[int, None], *args, **kwargs):
        res = await func(id, *args, **kwargs)
        if res is None:
            return None
        cache = KumikoCache(connection_pool=self.connection_pool)
        key = CommandKeyBuilder(
            prefix="cache",
            namespace="kumiko",
            id=id if id is not None else uuid.uuid4(),
            command=func.__name__,
        )

        if await cache.cacheExists(key=key) is False:
            await cache.setBasicCache(key=key, value=res, ttl=self.ttl)
            return res
        return await cache.getBasicCache(key=key)


class cacheJson:
    """
    A decorator to cache the result of a function that returns a `dict` to Redis.

    **Note**: The return type of the coroutine used has to be `dict`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        ttl (int, optional): TTL (Time-To-Live).
        Defaults to 30.
    """

    def __init__(self, connection_pool: ConnectionPool, ttl: int = 30):
        self.connection_pool = connection_pool
        self.ttl = ttl

    def __call__(self, func: Callable, *args: Any, **kwargs: Any):
        @wraps(func)
        async def wrapper(id: int, *args: Any, **kwargs: Any):
            return await self.deco(func, id, *args, **kwargs)

        return wrapper

    async def deco(self, func: Callable, id: Union[int, None], *args, **kwargs):
        res = await func(id, *args, **kwargs)
        if res is None:
            return None
        cache = KumikoCache(connection_pool=self.connection_pool)
        key = CommandKeyBuilder(
            prefix="cache",
            namespace="kumiko",
            id=id if id is not None else uuid.uuid4(),
            command=func.__name__,
        )

        if await cache.cacheExists(key=key) is False:
            await cache.setJSONCache(key=key, value=res, ttl=self.ttl)
            return res
        return await cache.getJSONCache(key=key)
