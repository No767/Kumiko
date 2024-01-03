from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

import discord
from async_lru import alru_cache

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore


@alru_cache(maxsize=256)
async def get_cached_prefix(
    bot: KumikoCore, message: discord.Message
) -> Union[str, List[str]]:
    base = [bot.default_prefix]
    if message.guild is None:
        get_cached_prefix.cache_invalidate(bot, message)
        return bot.default_prefix

    query = """
    SELECT prefix
    FROM guild
    WHERE id = $1;
    """
    prefixes = await bot.pool.fetchval(query, message.guild.id)
    if prefixes is None:
        get_cached_prefix.cache_invalidate(bot, message)
        return bot.default_prefix
    base.extend(item for item in prefixes)
    return base


async def get_prefix(bot: KumikoCore, msg: discord.Message) -> Union[str, List[str]]:
    if msg.guild is None:
        return bot.default_prefix
    cached_prefix = bot.prefixes.get(msg.guild.id)
    if cached_prefix is None:
        async with bot.pool.acquire() as conn:
            query = """
            SELECT prefix FROM guild WHERE id = $1;
            """
            update_query = """
            UPDATE guild
            SET prefix = $1
            WHERE id = $2;
            """
            fetch_prefix = await conn.fetchval(query, msg.guild.id)
            if fetch_prefix:
                bot.prefixes[msg.guild.id] = fetch_prefix
                return bot.prefixes[msg.guild.id]
            else:
                await conn.execute(update_query, [bot.default_prefix], msg.guild.id)
                bot.prefixes[msg.guild.id] = bot.default_prefix
                return bot.prefixes[msg.guild.id]
    else:
        return bot.prefixes[msg.guild.id]
