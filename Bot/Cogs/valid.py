from discord.ext import commands
from discord import Client
import discord
class valid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='valid')
    async def on_message(message, ctx):
        embedVar = discord.Embed(color = 14414079)
        embedVar.description = f'You are valid no matter what!'
        await ctx.send(embed = embedVar)
def setup(bot):
    bot.add_cog(valid(bot))
