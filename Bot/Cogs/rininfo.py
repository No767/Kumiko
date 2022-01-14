import discord
from discord.ext import commands
import asyncio
import uvloop


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rininfo", help="Server Info")
    async def on_message(self, ctx):
        bot = self.bot
        embedVar = discord.Embed(color=14414079)
        embedVar.set_author(name="Rin Info", icon_url=bot.user.avatar_url)
        embedVar.add_field(
            name="About",
            value="Rin is a discord bot which supports obtaining data from third party services such as DeviantArt, Hypixel, Reddit, MyAnimeList/Jikan, and many others. And you can request such data just from Discord. More services are planned to be supported, such as MangaDex, YT, Twitch, and many others. (The MangaDex service is planned for you to be able to read manga from Discord). If you are interested in a general-purpose version of Rin, check out Kumiko",
            inline=False,
        )
        embedVar.add_field(
            name="Getting Started",
            value="To help you get started, type in `.rinhelp` or `.help` in order to access the help page. This will provide you with all of the commands that is available to use as of now.",
            inline=False,
        )
        embedVar.add_field(
            name="Questions or Issues?",
            value="If you have any questions, or any issues, or just an idea that you would like to add, please report them on the [GitHub Issue Tracker](https://github.com/No767/Rin/issues). Note that Rin does not any type of support discord server nor do I plan to make one to begin with.",
        )
        embedVar.set_footer(
            text="Project Lead Maintainer and Original Creator of Rin: No767\nOriginal Creator of EasyBot.py and EasyBot Plugins: Chisaku-dev\n\nFun fact: use .version to check the current version of Rin"
        )
        await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def setup(bot):
    bot.add_cog(info(bot))
