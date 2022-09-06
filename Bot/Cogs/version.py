import asyncio

import discord
import uvloop
from discord.commands import slash_command
from discord.ext import commands


class VersionV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="version",
        description="Returns Current Version of Rin",
    )
    async def version(self, ctx):
        embedVar = discord.Embed()
        embedVar.description = "Build Version: v2.2.5"
        await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(VersionV1(bot))
