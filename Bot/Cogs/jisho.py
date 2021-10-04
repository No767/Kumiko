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

def hiragana(search):
    search = search.replace(" ", "%")
    result = jam.lookup(search)
    resulter = result.text(separator=" | ").replace(", ", " ")
    m = re.findall("[ぁ-ん]", resulter)
    all = str(m).replace(",", "")[1:-1]
    return all.replace("'", "").replace(" ", "")
    
def katakana(search):
    search = search.replace(" ", "%")
    result = jam.lookup(search)
    resulter = result.text(separator=" | ").replace(", ", " ")
    m = re.findall("[ァ-ン]", resulter)
    all = str(m).replace(",", "")[1:-1]
    return all.replace("'", "").replace(" ", "")

def kanji(search): 
    search = search.replace(" ", "%")
    result = jam.lookup(search)
    result_search = result.text(separator=" | ", with_chars=False).replace(", ", "")
    m = re.findall("[一-龯]", result_search)
    all_kanji = str(m).replace(",", "")[1:-1]
    return all_kanji.replace("'", "").replace(" ", "")
    
# Add Other English Definitions via JMDict's Low-Level SQL Feature 
def english_def_part1(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho_data = r.text
    jisho = json.loads(jisho_data)
    jisho_def = str(jisho['data'][0]['senses'][0]['english_definitions'])
    jisho_replacer = str(jisho_def.replace("'", " "))
    return jisho_replacer.replace("[", " ").replace("]", " ")

def tag(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho_data = r.text
    jisho = json.loads(jisho_data)
    jisho_tag = str(jisho['data'][0]['tags'])
    return jisho_tag.replace("[", " ").replace("]", " ").replace("'", " ")

def jlpt(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho_data = r.text
    jisho = json.loads(jisho_data)
    jisho_jlpt = str(jisho['data'][0]['tags'])
    return jisho_jlpt.replace("[", " ").replace("]", " ").replace("'", " ")

def is_common(search):
    search = search.replace(" ", "%20")
    link = f"https://jisho.org/api/v1/search/words?keyword={search}"
    r = requests.get(link)
    jisho_data = r.text
    jisho = json.loads(jisho_data)
    jishov1 = str(jisho['data'][0]['is_common'])
    return jishov1.replace("[", " ").replace("]", " ")

class jisho_dict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jisho")
    async def on_message(self, ctx, search: str):
        try:
            search = search.replace(" ", "%20")
            link = f"https://jisho.org/api/v1/search/words?keyword={search}"
            r = requests.get(link)
            jisho_data = r.text
            jisho = json.loads(jisho_data)
            embedVar = discord.Embed()
            embedVar.description = f"""
            Kanji >> {kanji(search)}
            Hiragana >> {hiragana(search)}
            Katakana >> {katakana(search)}
            
            English Def >> {english_def_part1(search)}
            Is Common? >> {is_common(search)}
            Tags >> {tag(search)}
            JLPT >> {jlpt(search)}
            
            **Attributions**
            
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