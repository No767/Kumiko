import discord
from discord.ext import commands


# removed the type hinting bc of circular imports
# if there is a way to solve it, then it would be back
async def get_prefix(bot, msg: discord.Message):
    if msg.guild is None:
        return commands.when_mentioned_or(bot.default_prefix)(bot, msg)
    try:
        return commands.when_mentioned_or(bot.prefixes[msg.guild.id])(bot, msg)
    except KeyError:
        # if not in the LRU cache
        async with bot.pool.acquire() as conn:
            query = """
            SELECT prefix FROM guild WHERE id = $1;
            """
            updateQuery = """
            UPDATE guild
            SET column = $1
            WHERE id = $2;
            """
            fetchPrefix = await conn.fetchval(query, msg.guild.id)
            if fetchPrefix:
                bot.prefixes[msg.guild.id] = fetchPrefix
                return commands.when_mentioned_or(bot.prefixes[msg.guild.id])(bot, msg)
            else:
                await conn.execute(updateQuery, bot.default_prefix, msg.guild.id)
                bot.prefixes[msg.guild.id] = bot.default_prefix
                return commands.when_mentioned_or(bot.prefixes[msg.guild.id])(bot, msg)
