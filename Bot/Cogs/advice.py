import json
import os
import re

import discord
import requests
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

def advice():
    link = f"https://api.adviceslip.com/advice"
    r = requests.get(link)
    advice_data = r.text
    advice = json.loads(advice_data)
    return advice

class advice_slip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="advice")
    async def on_message(self, ctx)
        advice_slip = advice()
        try:
            embedVar = discord.Embed()
            embedVar.description = f"{advice_slip['slip']['advice']}"
            await ctx.send(embed=embedVar)
        except:
            embedVar = discord.Embed()
            embedVar.description = "The query was unsuccessful"
            await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(advice_slip(bot))   