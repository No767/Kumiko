import asyncio
import datetime
import platform
import time

import discord
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands

VERSION = "v0.5.0"


class Kumiko(commands.Cog):
    """Commands to get basic info about Kumiko"""

    def __init__(self, bot):
        self.bot = bot

    kumiko = SlashCommandGroup("kumiko", "Commands About Kumiko")

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @kumiko.command(name="uptime")
    async def botUptime(self, ctx):
        """Returns uptime for Kumiko"""
        uptime = datetime.timedelta(seconds=int(round(time.time() - startTime)))
        embed = discord.Embed(color=discord.Color.from_rgb(245, 227, 255))
        embed.description = f"Kumiko's Uptime: `{uptime.days} Days, {uptime.seconds//3600} Hours, {(uptime.seconds//60)%60} Minutes, {(uptime.seconds%60)} Seconds`"
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @kumiko.command(name="info")
    async def kumikoInfo(self, ctx):
        """Shows some basic info about Kumiko"""
        embed = discord.Embed()
        embed.title = f"{self.bot.user.name} Info"
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="Server Count", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="User Count", value=len(self.bot.users), inline=True)
        embed.add_field(
            name="Python Version", value=platform.python_version(), inline=True
        )
        embed.add_field(name="Pycord Version", value=discord.__version__, inline=True)
        embed.add_field(name="Kumiko Build Version", value=VERSION, inline=True)
        await ctx.respond(embed=embed)

    @kumiko.command(name="version")
    async def version(self, ctx):
        """Returns the current version of Kumiko"""
        embedVar = discord.Embed()
        embedVar.description = f"Build Version: {VERSION}"
        await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @kumiko.command(name="ping")
    async def kumikoPing(self, ctx):
        """Returns Kumiko's Ping"""
        await ctx.respond(
            embed=discord.Embed(description=f"Ping: {self.bot.latency*1000:.2f}ms")
        )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(Kumiko(bot))
