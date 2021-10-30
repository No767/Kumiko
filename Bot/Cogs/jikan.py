import ujson

import requests
import discord
from discord.ext import commands

def get_anime_info(search):
    search = search.replace(" ", "%20")
    link = f"https://api.jikan.moe/v3/search/anime?q={search}"
    r = requests.get(link)
    return ujson.loads(r.text)

class JikanV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-search")
    async def anime(self, ctx, *, search:str):
        anime_info = get_anime_info(search)
        try: 
            embedVar = discord.Embed()
            embedVar.add_field(name="Title", value=anime_info["results"][0]["title"], inline=False)
            embedVar.add_field(name="Synopsis", value=anime_info["results"][0]["synopsis"], inline=False)
            embedVar.add_field(name="Episodes", value=anime_info["results"][0]["episodes"], inline=False)
            embedVar.add_field(name="Score", value=anime_info["results"][0]["score"], inline=False)
            embedVar.add_field(name="Start Date (airing)", value=anime_info["results"][0]["start_date"], inline=False)
            embedVar.add_field(name="End Date (airing)", value=anime_info["results"][0]["end_date"], inline=False)
            embedVar.add_field(name="MAL ID", value=anime_info["results"][0]["mal_id"], inline=False)
            embedVar.add_field(name="MAL URL", value=anime_info["results"][0]["url"], inline=False)
            embedVar.set_thumbnail(url=anime_info["results"][0]["image_url"])
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed()
            embedVar.description = f"The query could not be performed. Please try again.\nReason: {e}"
            await ctx.send(embed=embedVar)
            
def setup(bot):
    bot.add_cog(JikanV1(bot))