import uuid
from functools import wraps
from typing import Any, Callable, Optional, Union

from redis.asyncio.connection import ConnectionPool

from .redis_cache import CommandKeyBuilder, KumikoCache


class cache:
    """A decorator to cache the result of a function that returns a `str` to Redis.

    **Note**: The return type of the coroutine used has to be `str` or `bytes`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        ttl (int, optional): TTL (Time-To-Live). Defaults to 30.
    """

    def __init__(self, key: Optional[str] = None, ttl: int = 30):
        self.key = key
        self.ttl = ttl

    def __call__(self, func: Callable, *args: Any, **kwargs: Any):
        @wraps(func)
        async def wrapper(
            id: int, redis_pool: ConnectionPool, *args: Any, **kwargs: Any
        ):
            return await self.deco(func, id, redis_pool, *args, **kwargs)

        return wrapper

    async def deco(
        self,
        func: Callable,
        id: Union[int, None],
        redis_pool: ConnectionPool,
        *args,
        **kwargs
    ):
        res = await func(id, redis_pool, *args, **kwargs)
        if isinstance(res, str) is False:
            return None
        cache = KumikoCache(connection_pool=redis_pool)
        key = CommandKeyBuilder(
            prefix="cache",
            namespace="kumiko",
            id=id or self.key or uuid.uuid4(),  # type: ignore
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

    def __init__(self, key: Optional[str] = None, ttl: int = 30):
        self.key = key
        self.ttl = ttl

    def __call__(self, func: Callable, *args: Any, **kwargs: Any):
        @wraps(func)
        async def wrapper(
            id: int, redis_pool: ConnectionPool, *args: Any, **kwargs: Any
        ):
            return await self.deco(func, id, redis_pool, *args, **kwargs)

        return wrapper

    async def deco(
        self,
        func: Callable,
        id: Union[int, None],
        redis_pool: ConnectionPool,
        *args,
        **kwargs
    ):
        res = await func(id, *args, **kwargs)
        if isinstance(res, dict) is False:
            return None
        cache = KumikoCache(connection_pool=redis_pool)
        key = CommandKeyBuilder(
            prefix="cache",
            namespace="kumiko",
            id=id or self.key or uuid.uuid4(),  # type: ignore
            command=func.__name__,
        )

        if await cache.cacheExists(key=key) is False:
            await cache.setJSONCache(key=key, value=res, ttl=self.ttl)
            return res
        return await cache.getJSONCache(key=key)
