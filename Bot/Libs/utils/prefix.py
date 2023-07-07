from typing import List

import discord

# TODO - Prevent people from setting up `/` prefixes. Doesn't help
# removed the type hinting bc of circular imports
# if there is a way to solve it, then it would be back


async def get_prefix(bot, msg: discord.Message) -> List[str]:
    if msg.guild is None:
        return bot.default_prefix
        # return commands.when_mentioned_or(bot.default_prefix)(bot, msg)
    cachedPrefix = bot.prefixes.get(msg.guild.id)
    if cachedPrefix is None:
        async with bot.pool.acquire() as conn:
            query = """
            SELECT prefix FROM guild WHERE id = $1;
            """
            updateQuery = """
            UPDATE guild
            SET prefix = $1
            WHERE id = $2;
            """
            fetchPrefix = await conn.fetchval(query, msg.guild.id)
            if fetchPrefix:
                bot.prefixes[msg.guild.id] = fetchPrefix
                # return commands.when_mentioned_or(bot.prefixes[msg.guild.id])(bot, msg)
                return bot.prefixes[msg.guild.id]
            else:
                await conn.execute(updateQuery, [bot.default_prefix], msg.guild.id)
                bot.prefixes[msg.guild.id] = bot.default_prefix
                return bot.prefixes[msg.guild.id]
                # return commands.when_mentioned_or(bot.prefixes[msg.guild.id])(bot, msg)
    else:
        return bot.prefixes[msg.guild.id]
        # return commands.when_mentioned_or(bot.prefixes[msg.guild.id])(bot, msg)


def validatePrefix(prefixes: List[str], new_prefix: str) -> bool:
    """Validates whether the prefix given is valid or not.

    The rules for the prefix being valid goes as follows:

    1. The new prefix must not be in the prefixes list
    2. The new prefix cannot be "/".
        a. If a prefix containing "/" is followed with another character (eg "/e"), this is considered valid

    Args:
        prefixes (List[str]): The list of prefixes associated with the guild. This is usually found within the prefix cache
        new_prefix (str): The new prefix to validate

    Returns:
        bool: Whether the prefix is valid or not
    """
    return new_prefix in prefixes or (
        new_prefix.startswith("/") and len(new_prefix) == 1
    )
