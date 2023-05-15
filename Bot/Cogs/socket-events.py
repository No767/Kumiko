import discord
from discord.ext import commands
from kumikocore import KumikoCore
from prisma.models import Guild


class SocketEvents(commands.Cog):
    """Cog for handling socket events from Discord"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_guild_join")
    async def serverInit(guild: discord.Guild) -> None:  # type: ignore
        """Initializes the server in the database"""
        findGuild = await Guild.prisma().find_unique(where={"id": guild.id})
        if findGuild is None:
            await Guild.prisma().create({"id": guild.id})


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(SocketEvents(bot))
