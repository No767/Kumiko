from __future__ import annotations

from typing import TYPE_CHECKING, List, Union

import discord
from async_lru import alru_cache

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore


@alru_cache()
async def get_prefix(
    bot: KumikoCore, message: discord.Message
) -> Union[str, List[str]]:
    """Obtains the prefix for the guild

    This coroutine is heavily cached in order to reduce database calls
    and improved performance


    Args:
        bot (KumikoCore): An instance of `KumikoCore`
        message (discord.Message): The message that is processed

    Returns:
        Union[str, List[str]]: The default prefix or
        a list of prefixes (including the default)
    """
    base = [bot.default_prefix]
    if message.guild is None:
        get_prefix.cache_invalidate(bot, message)
        return bot.default_prefix

    query = """
    SELECT prefix
    FROM guild_config
    WHERE id = $1;
    """
    prefixes = await bot.pool.fetchval(query, message.guild.id)
    if prefixes is None:
        get_prefix.cache_invalidate(bot, message)
        return bot.default_prefix
    base.extend(item for item in prefixes)
    return base
