import os
import uuid
from typing import Dict, Union

from prisma.models import User
from redis.asyncio.connection import ConnectionPool

from ..cache import CommandKeyBuilder, MemoryCache, cachedJson

REDIS_HOST = (
    os.getenv("REDIS_HOST") if os.getenv("REDIS_HOST") is not None else "localhost"
)
REDIS_PORT = (
    int(os.getenv("REDIS_PORT")) if os.getenv("REDIS_PORT") is not None else 6379
)

connPool = ConnectionPool.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/0")

memCache = MemoryCache()
memCache.set(key="main", value=connPool)


@cachedJson(
    connection_pool=memCache.get(key="main"),
    command_key=CommandKeyBuilder(
        prefix="cache", namespace="kumiko", id=uuid.uuid4(), command="internal_get_user"
    ),
)
async def getUser(
    user_id: int, includes: Dict[str, bool] = {"inv": False, "marketplace": False}
) -> Union[Dict, None]:
    """[Coroutine] Helper coroutine to obtain a user's profile from the database

    For reducing the latency for accessing the data, this helper coroutine is cached on Redis (w/ RedisJSON). Also note that this coroutine expects that the Prisma query engine and database are already connected.

    Args:
        user_id (int): User ID to use to search up the user
        includes (Dict[str, bool], optional): Which schemas to include (for 1-n relations) Note that it must be a dict containing the column, and to include it or not. Defaults to {"inv": False, "marketplace": False}.

    Returns:
        Union[Dict, None]: The user's profile, or None if the user is not found
    """
    user = await User.prisma().find_unique(where={"id": user_id}, include=includes)
    return user.dict() if user is not None else None
