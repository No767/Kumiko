import asyncio

import aiohttp
import bs4
import discord
import orjson
import uvloop
from discord.commands import slash_command
from discord.ext import commands


class waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="waifu",
        description="Gives you a random waifu",
    )
    async def on_message(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
            }
            async with session.get(
                "https://www.mywaifulist.moe/random", headers=headers
            ) as r:
                data = await r.text()
                soup = bs4.BeautifulSoup(data, "lxml")
                waifu_title = soup.find("meta", attrs={"property": "og:title"}).attrs[
                    "content"
                ]
                image_url = soup.find("meta", attrs={"property": "og:image"}).attrs[
                    "content"
                ]
                description = soup.find("p", id="description").get_text()
                embedVar = discord.Embed(
                    title=waifu_title, color=discord.Color.from_rgb(208, 189, 255)
                )
                embedVar.description = f"{description}"
                embedVar.set_image(url=image_url)
                await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(waifu(bot))
