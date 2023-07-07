import logging
from typing import Literal

import asyncpg


async def ensureOpenPostgresConn(conn_pool: asyncpg.Pool) -> Literal[True]:
    """Ensures that the current connection pulled from the pool can be run.

    Args:
        conn_pool (asyncpg.Pool): The connection pool to get connections from.

    Returns:
        Literal[True]: If successful, the coroutine will return True, otherwise it will raise an exception
    """
    logger = logging.getLogger("discord")
    async with conn_pool.acquire() as conn:
        connStatus = conn.is_closed()
        if connStatus is False:
            logger.info("PostgreSQL server is up")
        return True
