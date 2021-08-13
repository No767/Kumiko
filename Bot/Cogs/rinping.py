import discord
from discord.ext import commands
from discord import Embed
class rinping(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(
        name='ping',
    )
    async def ping(self, ctx):
        await ctx.send(f'Ping >> {self.bot.latency} seconds')
    

def setup(bot):
    bot.add_cog(rinping(bot))