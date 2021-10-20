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
        [GitHub](https://github.com/No767/Rin) | [Docs](https://rin-docs.readthedocs.io/en/latest/) | Invite
        
        Welcome! Thanks for using this bot. As of now, it is under v0 Beta, but will be releasing soon if the project maintainer can find a place to officially host it. 
        """
        embedVar.set_author(name="Rin Info", icon_url=bot.user.avatar_url)
        embedVar.add_field(name="About", value="Rin is a Discord bot built with EasyBot.py plugin support. Its function is to be a general-purpose bot, which mostly focuses on third-party API support.", inline=False)
        embedVar.add_field(name="Getting Started", value="To help you get started, type in .rinhelp in order to access the help page. This will provide you with all of the commands that is available to use as of now.", inline=False)
        embedVar.set_footer(
            text="Project Lead Maintainer and Original Creator of Rin: No767\nOriginal Creator of EasyBot.py and EasyBot Plugins: Chisaku-dev"
        )
        await message.channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(info(bot))
