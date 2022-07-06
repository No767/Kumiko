import asyncio

import discord
import uvloop
from discord.commands import slash_command
from discord.ext import commands


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="rininfo", description="Info about Rin")
    async def rinInfo(self, ctx):
        bot = self.bot
        embedVar = discord.Embed(color=14414079)
        view = discord.ui.View(timeout=None)
        view.add_item(
            discord.ui.Button(label="GitHub", url="https://github.com/No767/Rin")
        )
        view.add_item(discord.ui.Button(label="Docs", url="https://docs.rinbot.live"))
        view.add_item(
            discord.ui.Button(
                label="Invite", url="https://top.gg/bot/865883525932253184/invite"
            )
        )
        embedVar.set_author(name="Rin Info", icon_url=bot.user.display_avatar)
        embedVar.add_field(
            name="About",
            value="Rin is a Discord bot focused on providing data from third party services such as DeviantArt, Hypixel, Reddit, MyAnimeList/Jikan, and many others with lighting speed. Rin allows you to find memes on Reddit with the Reddit service, or get info about your favorite anime with the MAL service. Under the hood, Rin uses [Uvloop](https://github.com/MagicStack/uvloop), which is 2x faster than Node.js and has the same performance as many Go programs. If you want a multipurpose version of Rin, check out Kumiko.",
            inline=False,
        )
        embedVar.add_field(
            name="Getting Started",
            value="To help you get started, type in `/rinhelp` in order to access the help page. This will provide you with all of the commands that is available to use as of now.",
            inline=False,
        )
        embedVar.add_field(
            name="Questions or Issues?",
            value="If you have any questions, or any issues, or just an idea that you would like to add, please report them on the [GitHub Issue Tracker](https://github.com/No767/Rin/issues). Note that Rin does not any type of support discord server nor do I plan to make one to begin with.",
        )
        embedVar.set_footer(
            text="Project Lead Maintainer and Original Creator of Rin: No767\nOriginal Creator of EasyBot.py and EasyBot Plugins: Isaac-To\n\nFun fact: use /version to check the current version of Rin"
        )
        await ctx.respond(embed=embedVar, view=view)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(info(bot))
