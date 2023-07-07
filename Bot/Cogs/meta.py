import datetime
import platform
import time

import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.utils import Embed

VERSION = "v0.9.0"


class Meta(commands.Cog):
    """Commands to obtain info about Kumiko or others"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U00002754")

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @commands.hybrid_command(name="uptime")
    async def botUptime(self, ctx: commands.Context) -> None:
        """Returns uptime for Kumiko"""
        uptime = datetime.timedelta(seconds=int(round(time.time() - startTime)))
        embed = Embed()
        embed.description = f"Kumiko's Uptime: `{uptime.days} Days, {uptime.seconds//3600} Hours, {(uptime.seconds//60)%60} Minutes, {(uptime.seconds%60)} Seconds`"
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="info")
    async def kumikoInfo(self, ctx: commands.Context) -> None:
        """Shows some basic info about Kumiko"""
        embed = Embed()
        embed.title = f"{self.bot.user.name} Info"  # type: ignore
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)  # type: ignore
        embed.add_field(name="Server Count", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="User Count", value=len(self.bot.users), inline=True)
        embed.add_field(
            name="Python Version", value=platform.python_version(), inline=True
        )
        embed.add_field(
            name="Discord.py Version", value=discord.__version__, inline=True
        )
        embed.add_field(name="Kumiko Build Version", value=VERSION, inline=True)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version")
    async def version(self, ctx: commands.Context) -> None:
        """Returns the current version of Kumiko"""
        embed = Embed()
        embed.description = f"Build Version: {VERSION}"
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """Returns the current latency of Kumiko"""
        embed = Embed()
        embed.description = f"Pong! {round(self.bot.latency * 1000)}ms"
        await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Meta(bot))
