from __future__ import annotations

from typing import TYPE_CHECKING, Union

from async_lru import alru_cache

if TYPE_CHECKING:
    import discord

    from core import Kumiko


@alru_cache(maxsize=1024)
async def get_prefix(bot: Kumiko, message: discord.Message) -> Union[str, list[str]]:
    """Obtains the prefix for the guild

    This coroutine is heavily cached in order to reduce database calls
    and improved performance


    Args:
        bot (Kumiko): An instance of `Kumiko`
        message (discord.Message): The message that is processed

    Returns:
        Union[str, List[str]]: The default prefix or
        a list of prefixes (including the default)
    """
    user_id = bot.user.id  # type: ignore

    # By putting the base with the mentions, we are effectively
    # doing the exact same thing as commands.when_mentioned
    base = [f"<@!{user_id}> ", f"<@{user_id}> ", bot.default_prefix]
    if message.guild is None:
        get_prefix.cache_invalidate(bot, message)
        return base

    query = """
    SELECT prefix
    FROM guild_prefix
    WHERE id = $1;
    """
    prefixes = await bot.pool.fetchval(query, message.guild.id)
    if prefixes is None:
        get_prefix.cache_invalidate(bot, message)
        return base
    base.extend(item for item in prefixes)
    return base
