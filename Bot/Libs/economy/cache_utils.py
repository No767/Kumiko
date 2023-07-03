from typing import Dict, Union

import asyncpg
from redis.asyncio.connection import ConnectionPool

from ..cache import cacheJson


# TODO - Add an join for the items owned
@cacheJson()
async def getUser(
    id: int, redis_pool: ConnectionPool, pool: asyncpg.Pool
) -> Union[Dict, None]:
    """[Coroutine] Helper coroutine to obtain a user's profile from the database

    For reducing the latency for accessing the data, this helper coroutine is cached on Redis (w/ RedisJSON).

    Args:
        id (int): User ID to use to search up the user
        redis_pool (ConnectionPool): Redis connection pool to use
        pool (asyncpg.Pool): Asyncpg pool

    Returns:
        Union[Dict, None]: The user's profile, or None if the user is not found
    """
    query = """
    SELECT rank, petals, created_at
    FROM eco_user
    WHERE id=$1;
    """
    async with pool.acquire() as conn:
        user = await conn.fetchval(query, id)
        if user is None:
            return None
        return dict(user)
