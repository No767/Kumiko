from typing import Optional


def CommandKeyBuilder(
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
