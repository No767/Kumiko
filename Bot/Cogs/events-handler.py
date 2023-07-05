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
        insertQuery = """
        INSERT INTO guild (id) VALUES ($1);
        INSERT INTO logging_config (guild_id) VALUES ($1);
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                exists = await conn.fetchval(existsQuery, guild.id)
                if not exists:
                    await conn.execute(insertQuery, guild.id)
                    self.bot.prefixes[guild.id] = [self.bot.default_prefix]

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("DELETE FROM guild WHERE id = $1", guild.id)
                self.bot.prefixes[guild.id] = self.bot.default_prefix

    # @commands.Cog.listener()
    # async def on_member_join(self, member: discord.Member) -> None:

    # @commands.Cog.listener()
    # async def on_log(self, member: discord.Member) -> None:
    #     channel = member.guild.get_channel(1125898205327007774)
    #     if isinstance(channel, discord.TextChannel):
    #         embed = JoinEmbed()
    #         # embed.set_author(name="Member Joined", icon_url=member.display_avatar.url)
    #         embed.title = "Member Joined"
    #         embed.set_thumbnail(url=member.display_avatar.url)
    #         embed.description = f"{member.mention} {member.global_name}"
    #         await channel.send(embed=embed)
    #         # await channel.send("hello")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsHandler(bot))
