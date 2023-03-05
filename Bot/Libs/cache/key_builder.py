import uuid
from typing import Optional, Union


def CommandKeyBuilder(
    prefix: Optional[str] = None,
    namespace: Optional[str] = None,
    id: Optional[Union[int, uuid.UUID]] = None,
    command: Optional[str] = None,
) -> str:
    """A key builder for commands

    Args:
        prefix (Optional[str], optional): Prefix of the key. Defaults to None.
        namespace (Optional[str], optional): Namespace of the key. Defaults to None.
        id (Optional[Union[int, uuid.UUID]], optional): Discord User or Guild ID. Or a UUID. Defaults to None.
        command (Optional[str], optional): Slash Command Name. Defaults to None.

    Returns:
        str: The key stored in Redis
    """
    return f"{prefix}:{namespace}:{id}:{command}"
