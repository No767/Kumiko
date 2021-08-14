import discord
from discord.ext import commands
from discord import client
from dotenv import load_dotenv
import deviantart
import os
import asyncio
import pytest

load_dotenv()
Client_ID = os.getenv("Client_ID")
Client_Secret = os.getenv("Client_Secret")
da = deviantart.Api(Client_ID, Client_Secret)

# the devartfetch gives out numbers, will need to get images instead
class devart(commands.Cog, discord.Client):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='devartfind')
    async def on_message(ctx):
        await ctx.send(da.browse(endpoint='hot'))
    async def on_error(ctx):
        await ctx.send("There seems to be an error. Please try again")
        
    @commands.command(name='devartsearch')
    @commands.Cog.listener('message')
    async def on_message(message, ctx):
        await ctx.send(f'What do you want to search for?')
        msg = await client.wait_for(message)
        await ctx.send(f'You have searched for {msg}')
        # await ctx.send(da.search_tags(msg))
        # devart_embed = discord.Embed()
        # devart_embed.description = f''
def setup(bot):
    bot.add_cog(devart(bot))