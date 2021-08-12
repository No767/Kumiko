import discord
from discord.ext import commands
from discord import client
from dotenv import load_dotenv
import deviantart
import os
load_dotenv()
Client_ID = os.getenv("Client_ID")
Client_Secret = os.getenv("Client_Secret")
da = deviantart.Api(Client_ID, Client_Secret)

# the devartfetch gives out numbers, will need to get images instead
class devart(commands.Cog, discord.Client):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(
        name = 'artbrowse'
    )
    async def on_message(message, ctx):
        await ctx.send(da.browse(endpoint='hot'))
    async def on_error(message, ctx):
        await ctx.send("There seems to be an error. Pleas try again")
        
    @commands.command(
        name = 'devartsearch'
    )
    async def on_message(message, ctx):
        await ctx.send(da.search_tags("Anime"))
def setup(bot):
    bot.add_cog(devart(bot))