import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.config import handle_guild_data


class EventsHandler(commands.Cog):
    """Cog for handling discord api events"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        insert_query = """
        WITH guild_insert AS (
            INSERT INTO guild (id) VALUES ($1)
            ON CONFLICT (id) DO NOTHING
        )
        INSERT INTO logging_config (guild_id) VALUES ($1)
        ON CONFLICT (guild_id) DO NOTHING;
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(insert_query, guild.id)
                await handle_guild_data(guild, conn, self.redis_pool)
                self.bot.prefixes[guild.id] = None

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        await self.pool.execute("DELETE FROM guild WHERE id = $1", guild.id)
        if guild.id in self.bot.prefixes:
            del self.bot.prefixes[guild.id]


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsHandler(bot))
