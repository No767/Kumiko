import discord
from discord.ext import commands
import datetime
class Rin_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="rininfo", help='Server Info')
    async def Rin_Info(self, message):
        embedVar = discord.Embed(title="Info", color=14414079, timestamp=datetime.datetime.now())
        embedVar.add_field(name="Command Prefix", value='Command Prefix is "**.**"')
        embedVar.add_field(name="Server Name", value=message.guild.name)
        await message.channel.send(embed=embedVar)

def setup(bot):
    bot.add_cog(Rin_Info(bot))