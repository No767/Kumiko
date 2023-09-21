from __future__ import annotations

from typing import TYPE_CHECKING, Dict

import asyncpg
from discord.ext import commands

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore


async def check_blacklist(ctx: commands.Context):
    bot = ctx.bot  # Pretty much returns the subclass anyways. I checked - Noelle
    if bot.owner_id == ctx.author.id or bot.application_id == ctx.author.id:
        return True

    blacklisted_status = await get_or_fetch_blacklist(bot, ctx.author.id, bot.pool)
    if blacklisted_status is True:
        # Get RickRolled lol
        # While implementing this, I was listening to Rick Astley
        await ctx.send(
            f"My fellow user, {ctx.author.mention}, you just got the L. You are blacklisted from using this bot. Take an \U0001f1f1, \U0001f1f1oser. [Here's how to appeal the blacklist.](https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
            suppress_embeds=True,
        )
        return False
    return True


async def load_blacklist(pool: asyncpg.Pool) -> Dict[int, bool]:
    """Loads the global blacklist into cache from the database

    Args:
        pool (asyncpg.Pool): A global connection pool

    Returns:
        Dict[int, str]: The cached mapping. Will be a 1:1 mapping of the data from the database.
    """
    query = """
    SELECT id, blacklist_status
    FROM blacklist;
    """
    records = await pool.fetch(query)
    return {record["id"]: record["blacklist_status"] for record in records}


# Circular import so bot is untyped
async def get_or_fetch_blacklist(bot: KumikoCore, id: int, pool: asyncpg.Pool) -> bool:
    """Gets or fetches a user's blacklist status

    Args:
        bot (KumikoCore): The bot instance
        id (int): The user's ID
        pool (asyncpg.Pool): A global connection pool

    Returns:
        bool: The user's blacklist status
    """
    if id in bot.blacklist_cache:
        return bot.blacklist_cache[id]

    query = """
    SELECT blacklist_status
    FROM blacklist
    WHERE id = $1;
    """
    record = await pool.fetchrow(query, id)
    if record is None:
        return False
    bot.blacklist_cache[id] = record["blacklist_status"]
    return record["blacklist_status"]
