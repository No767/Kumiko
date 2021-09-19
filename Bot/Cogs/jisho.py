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
        jisho = json.loads(jisho_data)
        embedVar = discord.Embed()
        
        
        embedVar.description = f"""
        Results: 
        
        **Result 1**
        
        Kanji >> {jisho['data'][0]['slug']}
        Hiragana >> {jisho['data'][0]['japanese'][0]['reading']}
        Katakana >> {jisho['data'][0]['japanese'][1]['reading']}
        
        
        English Def >> 

        Attributions
        JMDict >> {jisho['data'][0]['attribution']['jmdict']}
        JMNEDict >> {jisho['data'][0]['attribution']['jmnedict']}
        DBPedia >> {jisho['data'][0]['attribution']['dbpedia']}
        
        **Result 2**
        
        Kanji >> {jisho['data'][1]['slug']}


        

        
        **HTTP Status**
        HTTP Status Code >> {jisho['meta']['status']}
        
        
        """
        await ctx.send(embed=embedVar)

def setup(bot):
    bot.add_cog(jisho_dict(bot))
