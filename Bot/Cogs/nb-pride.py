import asyncio

import uvloop
from discord.ext import commands


class nbPride(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nb-pride")
    async def pride(self, ctx):
        reactions = [
            ":yellow_heart:",
            ":white_heart:",
            ":purple_heart:",
            ":black_heart:",
            ":transgender_flag:",
        ]
        for emoji in reactions:
            await ctx.send(emoji)


    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def setup(bot):
    bot.add_cog(nbPride(bot))