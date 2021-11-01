import bs4
import discord
import requests
from discord.ext import commands
from fake_useragent import UserAgent


class waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="waifu")
    async def on_message(self, ctx):
        headers = {"UserAgent": UserAgent().random}
        URL = "https://www.mywaifulist.moe/random"

        soup = bs4.BeautifulSoup(requests.get(
            URL, headers=headers).text, "html.parser")
        waifu_title = soup.find(
            "meta", attrs={"property": "og:title"}).attrs["content"]
        image_url = soup.find(
            "meta", attrs={"property": "og:image"}).attrs["content"]
        description = soup.find("p", id="description").get_text()
        embedVar = discord.Embed(
            title=waifu_title, color=discord.Color.from_rgb(208, 189, 255)
        )
        embedVar.description = f"{description}"
        embedVar.set_image(url=image_url)
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(waifu(bot))
