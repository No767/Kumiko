import asyncio
import datetime
import time

import discord
import uvloop
from discord.commands import slash_command
from discord.ext import commands


class UptimeV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()

    @slash_command(
        name="uptime",
        description="Returns Uptime for Rin",
    )
    async def botUptime(self, ctx):
        uptime = datetime.timedelta(
            seconds=int(round(time.time() - startTime)))
        embed = discord.Embed(color=discord.Color.from_rgb(245, 227, 255))
        embed.description = f"Rin's Uptime: `{uptime.days} Days, {uptime.seconds//3600} Hours, {(uptime.seconds//60)%60} Minutes, {(uptime.seconds%60)} Seconds`"
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(UptimeV1(bot))
