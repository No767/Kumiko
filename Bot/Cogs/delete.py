from discord.ext import commands
import discord
from discord import Embed
from discord import TextChannel

class deletemessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.command(name="rindelete")
    async def on_message(self, ctx):
        await ctx.delete(ctx)

class purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.is_owner()
    @commands.command(name="rinpurge")
    async def on_message(self, ctx):
        deleted = await ctx.delete()
        await ctx.send('Purged {} message(s)'.format(len(deleted)))

def setup(bot):
    bot.add_cog(deletemessage(bot))
    bot.add_cog(purge(bot))