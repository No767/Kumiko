import asyncio
import builtins
import logging
from typing import Literal, Union

import redis.asyncio as redis
from Libs.cache import MemoryCache
from redis.asyncio.connection import ConnectionPool
from redis.exceptions import ConnectionError, TimeoutError

from ..backoff import backoff

logger = logging.getLogger("discord")
backoffSec = 15
backoffSecIndex = 0


def setupRedisPool(
    host: str = "localhost", port: int = 6379, key: str = "main", timeout: float = 15.0
) -> None:
    """Sets up the Redis connection pool

    Args:
        host (str, optional): Redis host. Defaults to "localhost".
        port (int, optional): Redis port. Defaults to 6379.
        key (str, optional): The key of the mem cache. Defaults to "main".
        timeout (float, optional): Socket connection timeout. Defaults to 15.0.
    """
    connPool = ConnectionPool(
        host=host, port=port, db=0, socket_connect_timeout=timeout
    )
    builtins.memCache = MemoryCache()  # type: ignore
    builtins.memCache.add(key=key, value=connPool)  # type: ignore


async def pingRedis(connection_pool: ConnectionPool) -> bool:
    """Pings the redis server to ensure that it is alive

    Args:
        connection_pool (ConnectionPool): ConnectionPool object to use

    Returns:
        bool: Whether the Redis server is alive or not
    """
    r: redis.Redis = redis.Redis(connection_pool=connection_pool)
    return await r.ping()


async def redisCheck(
    host: str = "localhost",
    port: int = 6379,
    key: str = "main",
    timeout: float = 15.0,
    backoff_sec: int = 15,
    backoff_index: int = 0,
) -> Union[Literal[True], None]:
    """Integration method to check if the Redis server is alive

    Also sets up the conn pool cache. This is handled recursively actually.

    Args:
        host (str, optional): Redis host. Defaults to "localhost".
        port (int, optional): Redis port. Defaults to 6379.
        key (str, optional): The key of the mem cache. Defaults to "main".
        timeout (float, optional): Socket connection timeout. Defaults to 15.0.
        backoff_sec (int, optional): Backoff time in seconds. Defaults to 15.
        backoff_index (int, optional): Backoff index. This is used privately Defaults to 0.

    Returns:
        Union[Literal[True], None]: Returns True if the Redis server is alive. Returns None if the coroutine is in a recursive loop.
    """
    try:
        setupRedisPool(host=host, port=port, key=key, timeout=timeout)
        res = await pingRedis(connection_pool=builtins.memCache.get(key=key))  # type: ignore
        if res is True:
            logger.info("Successfully connected to Redis server")
            return True
    except (ConnectionError, TimeoutError):
        backoffTime = backoff(backoff_sec=backoff_sec, backoff_sec_index=backoff_index)
        logger.error(
            f"Failed to connect to Redis server - Restarting connection in {int(backoffTime)} seconds"
        )
        await asyncio.sleep(backoffTime)
        await redisCheck(
            host=host,
            port=port,
            key=key,
            timeout=timeout,
            backoff_sec=backoff_sec,
            backoff_index=backoff_index + 1,
        )
