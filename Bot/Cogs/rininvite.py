import asyncio

import discord
import uvloop
from discord.commands import slash_command
from discord.ext import commands


class InviteV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="invite", description="Invite links for Rin")
    async def invite(self, ctx):
        bot = self.bot
        embedVar = discord.Embed()
        embedVar.description = "[Top.gg](https://top.gg/bot/865883525932253184/invite)"
        embedVar.set_author(name="Invite", icon_url=bot.user.display_avatar)
        await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(InviteV1(bot))
