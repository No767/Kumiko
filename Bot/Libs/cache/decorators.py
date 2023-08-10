import uuid
from functools import wraps
from typing import Any, Callable, Optional, Union

from redis.asyncio.connection import ConnectionPool

from .redis_cache import KumikoCache, command_key_builder


class cache:
    """A decorator to cache the result of a function that returns a `str` to Redis.

    **Note**: The return type of the coroutine used has to be `str` or `bytes`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        ttl (int, optional): TTL (Time-To-Live). Defaults to 30.
    """

    def __init__(
        self, key: Optional[str] = None, ttl: int = 30, name: Optional[str] = None
    ):
        self.key = key
        self.ttl = ttl
        self.name = name

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
            return res
        cache = KumikoCache(connection_pool=redis_pool)
        key = self.key
        if key is None:
            key = command_key_builder(
                prefix="cache",
                namespace="kumiko",
                id=id or uuid.uuid4(),
                command=self.name or func.__name__,
            )

        if await cache.cache_exists(key=key) is False:
            await cache.set_basic_cache(key=key, value=res, ttl=self.ttl)
            return res
        return await cache.get_basic_cache(key=key)


class cache_json:
    """
    A decorator to cache the result of a function that returns a `dict` to Redis.

    **Note**: The return type of the coroutine used has to be `dict`

    Args:
        connection_pool (ConnectionPool): Redis connection pool to use
        ttl (int, optional): TTL (Time-To-Live). If None, then the TTL will not be set. Defaults to 30.
    """

    def __init__(
        self,
        key: Optional[str] = None,
        ttl: Union[int, None] = 30,
        name: Optional[str] = None,
        path: str = "$",
    ):
        self.key = key
        self.ttl = ttl
        self.name = name
        self.path = path

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
        if isinstance(res, dict) is False:
            return res
        cache = KumikoCache(connection_pool=redis_pool)
        key = self.key
        if key is None:
            key = command_key_builder(
                prefix="cache",
                namespace="kumiko",
                id=id or uuid.uuid4(),
                command=self.name or func.__name__,
            )

        if await cache.cache_exists(key=key) is False:
            await cache.set_json_cache(key=key, value=res, ttl=self.ttl)
            return res
        return await cache.get_json_cache(key=key, path=self.path)
