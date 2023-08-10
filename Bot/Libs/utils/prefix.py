from typing import List

import discord


async def get_prefix(bot, msg: discord.Message) -> List[str]:
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
