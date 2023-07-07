import logging

import discord
from discord.ext import commands
from discord.utils import utcnow
from kumikocore import KumikoCore
from Libs.utils import Embed


class EmbedCog(commands.Cog):
    """Embed test cog - Please only sync locally"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.hybrid_command(name="embed-time")
    async def embedTime(self, ctx: commands.Context) -> None:
        # await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name="you"),
        )
        # await ctx.send("set status to idle")
        embed = Embed()
        embed.timestamp = utcnow()
        self.logger.info(f"Timestamp: {embed.timestamp}")
        embed.set_footer(text=f"{embed.timestamp}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="embed-user")
    async def embedUser(self, ctx: commands.Context) -> None:

        await self.bot.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name="you"),
        )
        await ctx.send("set status to idle")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EmbedCog(bot))
