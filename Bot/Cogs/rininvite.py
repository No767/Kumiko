import discord
from discord.ext import commands
import asyncio
import uvloop


class InviteV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rininvite", aliases=["invite"])
    async def invite(self, ctx):
        bot = self.bot
        embedVar = discord.Embed()
        embedVar.description = "[Top.gg](https://top.gg/bot/865883525932253184/invite)\n[Fallback URL](https://discord.com/api/oauth2/authorize?client_id=865883525932253184&permissions=150055930992&scope=bot)"
        embedVar.set_author(name="Invite", icon_url=bot.user.avatar_url)
        await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(InviteV1(bot))
