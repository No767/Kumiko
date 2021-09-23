import json

import discord
import requests
from discord import Embed
from discord.ext import commands
import re
from dotenv import load_dotenv
import os

load_dotenv()

class jisho_dict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jisho")
    async def on_message(self, ctx, search: str):
        search = search.replace(" ", "%20")
        link = f"https://jisho.org/api/v1/search/words?keyword={search}"
        kanji_url = f"https://kanjialive-api.p.rapidapi.com/api/public/search/{search}"
        headers = {
            'x-rapidapi-host': "kanjialive-api.p.rapidapi.com",
            'x-rapidapi-key': f"{os.getenv('Rapid_API_Key')}"
        }
        r = requests.get(link)
        jisho_data = r.text
        jisho = json.loads(jisho_data)
        kanji_alive = requests.request("GET", kanji_url, headers=headers)
        kanji_parser = json.loads(kanji_alive.text)
        

        
        embedVar = discord.Embed()
        embedVar.description = f"""
        Results: 
        Kanji >> {str(kanji_parser).split(", ")}


        Attributions
        JMDict >> {jisho['data'][0]['attribution']['jmdict']}
        JMNEDict >> {jisho['data'][0]['attribution']['jmnedict']}
        DBPedia >> {jisho['data'][0]['attribution']['dbpedia']}
        
        **HTTP Status**
        HTTP Status Code >> {jisho['meta']['status']}
        
        
        """
        await ctx.send(embed=embedVar)
        

        
    


    
def setup(bot):
    bot.add_cog(jisho_dict(bot))
