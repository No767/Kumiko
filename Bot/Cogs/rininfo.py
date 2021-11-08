import discord
from discord.ext import commands


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rininfo", help="Server Info")
    async def on_message(self, message):
        bot = self.bot
        embedVar = discord.Embed(color=14414079)
        embedVar.description = """
        **[GitHub](https://github.com/No767/Rin)** | **[Issue Tracker](https://github.com/No767/Rin/issues)** | **[Docs](https://rin-docs.readthedocs.io/en/latest/)** | **[Invite](https://top.gg/bot/865883525932253184/invite)**
        """
        embedVar.set_author(name="Rin Info", icon_url=bot.user.avatar_url)
        embedVar.add_field(
            name="Welcome!",
            value="Thanks for using this bot. Rin is officially ready for production use.",
            inline=False,
        )
        embedVar.add_field(
            name="About",
            value="Rin is a Discord bot built with EasyBot.py plugin support. Its function is to be a general-purpose bot, which mostly focuses on third-party API support. Some of them include Hypixel, MyAnimeList, Instagram, and many others.",
            inline=False,
        )
        embedVar.add_field(
            name="Getting Started",
            value="To help you get started, type in .rinhelp in order to access the help page. This will provide you with all of the commands that is available to use as of now.",
            inline=False,
        )
        embedVar.set_footer(
            text="Project Lead Maintainer and Original Creator of Rin: No767\nOriginal Creator of EasyBot.py and EasyBot Plugins: Chisaku-dev"
        )
        await message.channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(info(bot))
