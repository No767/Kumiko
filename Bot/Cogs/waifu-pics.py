import asyncio
import random

import aiohttp
import discord
import orjson
import uvloop
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
                waifu_pics = await r.json()
                try:
                    await ctx.send(waifu_pics["url"])
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful"
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(waifu(bot))
