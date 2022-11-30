import uuid
from typing import Optional


def defaultKeyBuilder(
    prefix: Optional[str] = None,
    namespace: Optional[str] = None,
    user_id: Optional[int] = None,
) -> str:
    """Builds a default key used in Redis

    Builds a default key with the following: `prefix:namespace:uuid4:user_id`

    Args:
        prefix (Optional[str], optional): Prefix of key. Defaults to "".
        namespace (Optional[str], optional): Namespace used for key. Defaults to "".
        user_id (Optional[int], optional): Discord User ID. Defaults to None.

    Returns:
        str: Key stored in Redis
    """
    return f"{prefix}:{namespace}:{str(uuid.uuid4())}:{user_id}"


def commandKeyBuilder(
    prefix: Optional[str] = None,
    namespace: Optional[str] = None,
    id: Optional[int] = None,
    command: Optional[str] = None,
) -> str:
    """A key builder for commands

    Args:
        prefix (Optional[str], optional): Prefix of the key. Defaults to None.
        namespace (Optional[str], optional): Namespace of the key. Defaults to None.
        id (Optional[int], optional): Discord User or Guild ID. Defaults to None.
        command (Optional[str], optional): Slash Command Name. Defaults to None.

    Returns:
        str: The key stored in Redis
    """
    return f"{prefix}:{namespace}:{id}:{command}"
