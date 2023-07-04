import discord
from discord.ext import commands
from kumikocore import KumikoCore


class EventsHandler(commands.Cog):
    """Cog for handling discord api events"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        existsQuery = "SELECT EXISTS(SELECT 1 FROM guild WHERE id = $1);"
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                exists = await conn.fetchval(existsQuery, guild.id)
                if not exists:
                    await conn.execute("INSERT INTO guild (id) VALUES ($1)", guild.id)
                    self.bot.prefixes[guild.id] = [self.bot.default_prefix]

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("DELETE FROM guild WHERE id = $1", guild.id)
                self.bot.prefixes[guild.id] = self.bot.default_prefix


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsHandler(bot))
