from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union

import asyncpg
import discord
from async_lru import alru_cache
from discord.ext import commands

from .message_constants import MessageConstants

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore


class BlacklistEntity:
    __slots__ = ("id", "blacklist_status", "unknown_entity")

    def __init__(self, record: Optional[asyncpg.Record] = None):
        self.unknown_entity = True

        if record:
            self.id = record["id"]
            self.blacklist_status = record["blacklist_status"]
            self.unknown_entity = False


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


async def check_blacklist(ctx: commands.Context) -> bool:
    bot = ctx.bot  # Pretty much returns the subclass anyways. I checked - Noelle
    if bot.owner_id == ctx.author.id or bot.application_id == ctx.author.id:
        return True

    blacklist = await get_blacklist(ctx.author.id)

    if blacklist.blacklist_status is True and blacklist.unknown_entity is False:
        # Get RickRolled lol
        # While implementing this, I was listening to Rick Astley
        await ctx.send(
            f"My fellow user, {ctx.author.mention}, you just got the L. {MessageConstants.BLACKLIST_APPEAL_MSG.value}",
            suppress_embeds=True,
        )
        return False
    return True


async def check_blacklist_interaction(interaction: discord.Interaction) -> bool:
    bot: KumikoCore = interaction.client  # type: ignore # Checked and it is that
    if bot.owner_id == interaction.user.id or bot.application_id == interaction.user.id:
        return True

    blacklist = await get_blacklist(interaction.user.id)

    if blacklist.blacklist_status is True and blacklist.unknown_entity is False:
        await interaction.response.send_message(
            f"My fellow user, {interaction.user.mention}, you just got the L. {MessageConstants.BLACKLIST_APPEAL_MSG.value}",
            suppress_embeds=True,
        )
        return False
    return True


# async def load_blacklist(pool: asyncpg.Pool) -> Dict[int, bool]:
#     """Loads the global blacklist into cache from the database

#     Args:
#         pool (asyncpg.Pool): A global connection pool

#     Returns:
#         Dict[int, str]: The cached mapping. Will be a 1:1 mapping of the data from the database.
#     """
#     query = """
#     SELECT id, blacklist_status
#     FROM blacklist;
#     """
#     records = await pool.fetch(query)
#     formatted_records = {record["id"]: record["blacklist_status"] for record in records}
#     return formatted_records


# async def get_or_fetch_blacklist(bot: KumikoCore, id: int, pool: asyncpg.Pool) -> bool:
#     """Gets or fetches a user's blacklist status

#     Args:
#         bot (KumikoCore): The bot instance
#         id (int): The user's ID
#         pool (asyncpg.Pool): A global connection pool

#     Returns:
#         bool: The user's blacklist status
#     """
#     if id in bot.blacklist_cache:
#         return bot.blacklist_cache[id]

#     query = """
#     SELECT blacklist_status
#     FROM blacklist
#     WHERE id = $1;
#     """
#     record = await pool.fetchrow(query, id)
#     if record is None:
#         return False
#     bot.blacklist_cache[id] = record["blacklist_status"]
#     return record["blacklist_status"]


# async def get_or_fetch_full_blacklist(
#     bot: KumikoCore, pool: asyncpg.Pool
# ) -> Optional[Dict[int, bool]]:
#     cache = bot.blacklist_cache

#     # We can guarantee these to be 1:1 mappings
#     if len(cache) != 0:
#         return cache

#     query = """
#     SELECT id, blacklist_status
#     FROM blacklist;
#     """
#     records = await pool.fetch(query)
#     if len(records) == 0:
#         return None

#     converted_records: Dict[int, bool] = {
#         record["id"]: record["blacklist_status"] for record in records
#     }
#     bot.replace_blacklist_cache(converted_records)
#     return converted_records
