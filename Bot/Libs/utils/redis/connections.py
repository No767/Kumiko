import asyncio
import logging
from typing import Literal, Union

import redis.asyncio as redis
from Libs.cache import kumikoCP
from redis.asyncio.connection import ConnectionPool
from redis.exceptions import ConnectionError, TimeoutError

from ..backoff import backoff

logger = logging.getLogger("discord")


async def pingRedis(connection_pool: ConnectionPool) -> bool:
    """Pings the redis server to ensure that it is alive

    Args:
        connection_pool (ConnectionPool): ConnectionPool object to use

    Returns:
        bool: Whether the Redis server is alive or not
    """
    r: redis.Redis = redis.Redis(connection_pool=connection_pool, socket_timeout=10.0)
    return await r.ping()


async def redisCheck(
    backoff_sec: int = 15,
    backoff_index: int = 0,
) -> Union[Literal[True], None]:
    """Integration method to check if the Redis server is alive

    Also sets up the conn pool cache. This is handled recursively actually.

    Args:
        backoff_sec (int, optional): Backoff time in seconds. Defaults to 15.
        backoff_index (int, optional): Backoff index. This is used privately Defaults to 0.

    Returns:
        Union[Literal[True], None]: Returns True if the Redis server is alive. Returns None if the coroutine is in a recursive loop.
    """
    try:
        connPool = kumikoCP.getConnPool()
        res = await pingRedis(connection_pool=connPool)
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
            backoff_index=backoff_index + 1,
        )
