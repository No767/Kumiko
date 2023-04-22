from typing import Dict, Union

from prisma.models import User
from prisma.types import UserInclude

from ..cache import cacheJson, kumikoCP


@cacheJson(connection_pool=kumikoCP.getConnPool())
async def getUser(id: int, includes: UserInclude) -> Union[Dict, None]:
    """[Coroutine] Helper coroutine to obtain a user's profile from the database

    For reducing the latency for accessing the data, this helper coroutine is cached on Redis (w/ RedisJSON). Also note that this coroutine expects that the Prisma query engine and database are already connected.

    Args:
        id (int): User ID to use to search up the user
        includes (UserInclude, optional): Which schemas to include (for 1-n relations) Note that it must be a dict containing the column, and to include it or not.

    Returns:
        Union[Dict, None]: The user's profile, or None if the user is not found
    """
    user = await User.prisma().find_unique(where={"id": id}, include=includes)
    return user.dict() if user is not None else None
