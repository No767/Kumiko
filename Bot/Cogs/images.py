import random

import bs4
import requests
from discord.ext import commands


# get link and prepare for scraping
def image_scrape(link):
    htmldata = requests.get(link).text
    soup = bs4.BeautifulSoup(htmldata, "html.parser")
    # find all imgs
    links = []
    for item in soup.find_all("img"):
        # if src is the link
        if (
            "avatar" not in item["src"]
            and "hover" not in item["src"]
            and "logo" not in item["src"]
            and "icon" not in item["src"]
            and "data" not in item["src"]
        ):
            if "//" in item["src"]:
                links.append(item["src"])
            else:
                # takes domain name and adds back src to complete link
                links.append("https://" + link.split("/")[2] + item["src"])
        # print all links
    return random.choice(links)


class deviantart_images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="image", help="searches for an image on deviantart images")
    async def image(self, ctx, *, search: str):
        search = search.replace(" ", "%20")
        link = f"https://www.deviantart.com/search?q={search}"
        image_link = image_scrape(link)
        await ctx.send(image_link)


def setup(bot):
    bot.add_cog(deviantart_images(bot))
