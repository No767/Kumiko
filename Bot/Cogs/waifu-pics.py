import random

import aiohttp
import discord
import ujson
import orjson
from discord.ext import commands


class waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="waifupics", aliases=["wp"])
    async def on_messsage(self, ctx):
        waifu_list = [
            "waifu",
            "neko",
            "shinobu",
            "megumin",
            "bully",
            "cuddle",
            "cry",
            "hug",
            "awoo",
            "kiss",
            "lick",
            "pat",
            "smug",
            "bonk",
            "yeet",
            "blush",
            "smile",
            "wave",
            "highfive",
            "handhold",
            "nom",
            "bite",
            "glomp",
            "slap",
            "kill",
            "kick",
            "happy",
            "wink",
            "poke",
            "dance",
            "cringe",
        ]
        searchterm = random.choice(waifu_list)
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.waifu.pics/sfw/{searchterm}") as r:
                waifu_pics = await r.text()
                waifu_pics_formatted = orjson.loads(waifu_pics)
                try:
                    await ctx.send(waifu_pics_formatted["url"])
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful"
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(waifu(bot))
