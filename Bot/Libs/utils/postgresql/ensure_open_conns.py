import logging

import asyncpg


async def ensureOpenPostgresConn(conn_pool: asyncpg.Pool) -> bool:
    """Ensures that the current connection pulled from the pool can be run.

    Args:
        conn_pool (asyncpg.Pool): The connection pool to get connections from.

    Returns:
        bool: True if the connection can be ran.
    """
    logger = logging.getLogger("discord")
    async with conn_pool.acquire() as conn:
        connStatus = conn.is_closed()
        if connStatus is False:
            logger.info("PostgreSQL server is up")
            return True
    logger.error("Failed to connect to PostgreSQL")
    return False