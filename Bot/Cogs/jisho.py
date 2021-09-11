import json

import discord
import requests
from discord import Embed
from discord.ext import commands


class jisho_dict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jisho")
    async def on_message(self, ctx, search: str):
        search = search.replace(" ", "%20")
        link = f"https://jisho.org/api/v1/search/words?keyword={search}"
        r = requests.get(link)
        jisho_data = r.text
        jisho_parser = json.loads(jisho_data)
        embedVar = discord.Embed()
        embedVar.description = f"""
        First Word: {jisho_parser['data'][0]['japanese'][0]['reading']}
        
        Senses: {jisho_parser['data'][0]['senses'][0]['english_definitions']}
        
        
        
        
        
        """
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(jisho_dict(bot))
