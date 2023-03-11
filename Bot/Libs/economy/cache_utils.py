import builtins
import uuid
from typing import Dict, Union

from prisma.models import User
from redis.asyncio.connection import ConnectionPool

from ..cache import CommandKeyBuilder, cachedJson
from ..utils.redis import setupRedisPool


def getConnPool() -> ConnectionPool:
    """[Function] Helper function to obtain the connection pool for Redis

    Returns:
        ConnectionPool: The connection pool for Redis
    """
    if not hasattr(builtins, "memCache"):
        setupRedisPool()
    return builtins.memCache.get(key="main")


@cachedJson(
    connection_pool=getConnPool(),
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
