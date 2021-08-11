import discord
from discord.ext import commands
import datetime
class rininfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def rininfo(self, message):
        embedVar = discord.Embed(title="Info", color=14414079, timestamp=datetime.datetime.now())
        embedVar.add_field(name="Command Prefix", value='Command Prefix is "**.**"')
        embedVar.add_field(name="Server Name", value=message.guild.name)
        await message.channel.send(embed=embedVar)

def setup(bot):
    bot.add_cog(rininfo(bot))