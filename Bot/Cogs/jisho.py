import json

import discord
import requests
from discord import Embed
from discord.ext import commands
import re

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
        english_def = jisho_parser['data'][0]['senses'][0]['english_definitions'][1:-1]
        embedVar = discord.Embed()
        
        
        embedVar.description = f"""
        Results: 
        
        **Result 1**
        
        Kanji >> {jisho_parser['data'][0]['slug']}
        Hiragana >> {jisho_parser['data'][0]['japanese'][0]['reading']}
        Katakana >> {jisho_parser['data'][0]['japanese'][1]['reading']}
        
        
        English Def >> {english_def}

        Attributions
        JMDict >> {jisho_parser['data'][0]['attribution']['jmdict']}
        JMNEDict >> {jisho_parser['data'][0]['attribution']['jmnedict']}
        DBPedia >> {jisho_parser['data'][0]['attribution']['dbpedia']}
        
        **Result 2**
        
        


        

        
        **HTTP Status**
        HTTP Status Code >> {jisho_parser['meta']['status']}
        
        
        """
        await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(jisho_dict(bot))
