import logging
from typing import Literal

import asyncpg
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool


async def ensure_postgres_conn(pool: asyncpg.Pool) -> Literal[True]:
    """Ensures that the current connection pulled from the PostgreSQL pool can be run.

    Args:
        pool (asyncpg.Pool): The connection pool to get connections from.

    Returns:
        Literal[True]: If successful, the coroutine will return True, otherwise it will raise an exception
    """
    logger = logging.getLogger()
    async with pool.acquire() as conn:
        res = conn.is_closed()
        if res is False:
            logger.info("Successfully connected to the PostgreSQL server")
        return True


async def ensure_redis_conn(redis_pool: ConnectionPool) -> Literal[True]:
    """Pings the Redis server to check if it's open or not

    Args:
        connection_pool (Union[ConnectionPool, None]): The supplied connection pool. If none, it will be created automatically

    Returns:
        Literal[True]: If successful, the coroutine will return True, otherwise it will raise an exception
    """
    logger = logging.getLogger()
    r: redis.Redis = redis.Redis(connection_pool=redis_pool)
    res = await r.ping()
    if res:
        logger.info("Successfully connected to the Redis server")
    return True
