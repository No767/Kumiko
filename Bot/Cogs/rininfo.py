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
        [GitHub](https://github.com/No767/Rin) | [Docs](https://rin-docs.readthedocs.io/en/latest/)
        
        Welcome! Thanks for using this bot. As of now, it is under v0 Beta, but will be releasing soon if the project maintainer can find a place to officially host it. 
        
        Rin is a Discord bot built with EasyBot.py plugin support. Its function is to be a general-purpose bot, which mostly focuses on third-party API support.
        """
        embedVar.set_author(name="Rin Info", icon_url=bot.user.avatar_url)
        embedVar.set_footer(
            text="Project Lead Maintainer and Original Creator: No767")
        await message.channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(info(bot))
