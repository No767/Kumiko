import logging

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

logger = logging.getLogger("discord")


async def ensureOpenRedisConn(redis_pool: ConnectionPool) -> bool:
    """Pings the Redis server to check if it's open or not

    Args:
        connection_pool (Union[ConnectionPool, None]): The supplied connection pool. If none, it will be created automatically

    Returns:
        bool: Whether the server is up or not
    """
    r: redis.Redis = redis.Redis(connection_pool=redis_pool)
    resultPing = await r.ping()
    if resultPing:
        logger.info("Sucessfully connected to the Redis server")
        return True
    logger.error("Failed to connect to the Redis server - Restart Kumiko to reconnect")
    return False
