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
        
        English Def: {jisho_parser['data'][0]['senses'][0]['english_definitions']}
        
        Parts of speech: {jisho_parser['data'][0]['senses'][0]['parts_of_speech']}
        
        Tags? >> {jisho_parser['data'][0]['tags']}
        
        ---
        
        The second word: {jisho_parser['data'][1]['japanese'][0]['reading']}
        
        That second word's english writing: {jisho_parser['data'][1]['senses'][1]['english_definitions']}
        
        
        Parts of speech: {jisho_parser['data'][1]['senses'][1]['parts_of_speech']}
        
        Tags >> {jisho_parser['data'][1]['senses'][1]['tags']}
        
        --- 
        That goddamn third word (kanji): {jisho_parser['data'][2]['japanese'][0]['word']} # May replace that with the slug of each python dict. Currently broken
         
        Hiragana: {jisho_parser['data'][2]['japanese'][0]['reading']}
        
        Katakana: {jisho_parser['data'][2]['japanese'][1]['reading']}
        
        English Def: {jisho_parser['data'][2]['senses'][0]['english_definitions']}
        
        Parts of Speech: {jisho_parser['data'][2]['senses'][0]['parts_of_speech']}
        
        tags: {jisho_parser['data'][2]['senses'][0]['tags']}
        """
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(jisho_dict(bot))
