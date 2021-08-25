import discord
from discord.ext import commands
import datetime


class rininfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rininfo", help="Server Info")
    async def rininfo(self, message):
        bot = self.bot
        name = bot.user.name
        id = bot.user.id
        embedVar = discord.Embed(title="Rin Info", color=14414079)
        embedVar.description = f"""
        Welcome! Thanks for using this bot, and as of now, it is under heavy development.
        
        The Rin bot is a Discord bot built on top of EasyBot.py, and allows for EasyBot.py plugins to be supported. Its function is to be a general-purpose bot, which mostly focuses on games, and other third-party API support.
        
        GitHub: https://github.com/No767/Rin
        
        Docs: https://rin-docs.readthedocs.io/en/latest/
        """
        embedVar.set_thumbnail(url=bot.user.avatar_url)
        await message.channel.send(embed=embedVar)


def setup(bot):
    bot.add_cog(rininfo(bot))
