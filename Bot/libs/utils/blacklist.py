from __future__ import annotations

from typing import Optional, Union

import asyncpg
import discord
from async_lru import alru_cache
from discord import Enum


class BlacklistEntityType(Enum):
    user = 0
    guild = 1


class BlacklistEntity:
    __slots__ = ("id", "entity_id", "entity_type", "status")

    def __init__(self, record: Optional[asyncpg.Record] = None):
        self.id = None

        if record:
            self.id = record["id"]
            self.entity_id = record["entity_id"]
            self.entity_type = BlacklistEntityType(record["entity_type"])
            self.status = record["status"]


@alru_cache(maxsize=256)
async def get_blacklist(
    user: Union[discord.User, discord.Member],
    guild: Optional[discord.Guild],
    connection: Union[asyncpg.Connection, asyncpg.Pool],
) -> Optional[BlacklistEntity]:
    """Obtains an blacklist entity from the database

    Args:
        id (int): The ID used to check
        connection (Union[asyncpg.Connection, asyncpg.Pool]): Asyncpg connection

    Returns:
        BlacklistEntity: A entity representing a blacklist entry
    """
    query = """
    SELECT id, entity_id, entity_type, status
    FROM blacklist
    WHERE entity_id = $1 OR $2;
    """
    guild_id = guild.id if guild is not None else None
    record = await connection.fetchrow(query, user.id, guild_id)
    if record is None:
        get_blacklist.cache_invalidate(user, guild, connection)
        return None
    return BlacklistEntity(record=record)
