import json
import os
import re

import discord
import requests
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv
from jamdict import Jamdict

load_dotenv()
jam = Jamdict()

def english_def_parser(search):
    search = search.replace(" ", "%")
    result = jam.lookup(search)
    for word in result.entries:
        return list(word)
    
def kanji_finder(search): 
    search = search.replace(" ", "%")
    result = jam.lookup(search)
    for c in result.chars:
        searcher = re.search("^\w", repr(c))
        return searcher.group(0)
    
class jisho_dict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jisho")
    async def on_message(self, ctx, search: str):
        try:
            search = search.replace(" ", "%20")
            link = f"https://jisho.org/api/v1/search/words?keyword={search}"
            kanji_url = (
                f"https://kanjialive-api.p.rapidapi.com/api/public/search/{search}" # May not need Kanji Alive since JMDict is replacing that for the Kanji lookup
            )
            headers = {
                "x-rapidapi-host": "kanjialive-api.p.rapidapi.com",
                "x-rapidapi-key": f"{os.getenv('Rapid_API_Key')}",
            }
            r = requests.get(link) # Only use Jisho for english def
            jisho_data = r.text
            jisho = json.loads(jisho_data)
            kanji_alive = requests.request("GET", kanji_url, headers=headers)
            kanji_parser = json.loads(kanji_alive.text)

            embedVar = discord.Embed()
            embedVar.description = f"""
            Results: 

            Kanji >> {kanji_finder(search)}
            
            
            English Def >> {english_def_parser(search)}
            Attributions
            JMDict >> {jisho['data'][0]['attribution']['jmdict']}
            JMNEDict >> {jisho['data'][0]['attribution']['jmnedict']}
            DBPedia >> {jisho['data'][0]['attribution']['dbpedia']}

            **HTTP Status**
            HTTP Status Code >> {jisho['meta']['status']}


            """
            await ctx.send(embed=embedVar)
        except:
            embed_discord = discord.Embed()
            embed_discord.description = 'An error has occurred. Please try again'
            await ctx.send(embed=embed_discord)



def setup(bot):
    bot.add_cog(jisho_dict(bot))
