from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

import asyncpg
from async_lru import alru_cache

if TYPE_CHECKING:
    pass


class BlacklistEntity:
    __slots__ = ("id", "blacklist_status", "unknown_entity")

    def __init__(self, record: Optional[asyncpg.Record] = None):
        self.blacklist_status = None

        if record:
            self.id = record["id"]
            self.blacklist_status = record["blacklist_status"]


@alru_cache(maxsize=256)
async def get_blacklist(
    id: int, connection: Union[asyncpg.Connection, asyncpg.Pool]
) -> BlacklistEntity:
    """Obtains an blacklist entity from the database

    Args:
        id (int): The ID used to check
        connection (Union[asyncpg.Connection, asyncpg.Pool]): Asyncpg connection

    Returns:
        BlacklistEntity: A entity representing a blacklist entry
    """
    query = """
    SELECT id, blacklist_status
    FROM blacklist
    WHERE id = $1;
    """
    record = await connection.fetchrow(query, id)
    if record is None:
        return BlacklistEntity()
    return BlacklistEntity(record=record)
