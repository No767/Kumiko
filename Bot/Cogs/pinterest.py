import json
import os
import random

import discord
import requests
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class pinterest_api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="pinterestsearch")
    async def on_message(self, ctx):
        await ctx.send("The Pinterest Cog is under development rn. Please come back later")

def setup(bot):
    bot.add_cog(pinterest_api(bot))
