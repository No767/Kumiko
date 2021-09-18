import bs4
import discord
from discord.ext import commands
from discord import Embed
import requests
import random

def pixiv2(link):
    data = requests.get(link).text
    soup = bs4.BeautifulSoup(data, "lxml")
    links = []
    soup.find_all("img")
    
    
class pixiv_scrapper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='pixiv')
    async def on_message(self, ctx, search:str):
        image_link = f"https://www.pixiv.net/en/tags/{search}"
        search = search.replace(" ", "%20")
        htmldata = requests.get(image_link).text
        soup = bs4.BeautifulSoup(htmldata, "html.parser")
        links = []
        for item in soup.find_all('img'):
            await ctx.send(item["src"])

        
def setup(bot):
    bot.add_cog(pixiv_scrapper(bot))