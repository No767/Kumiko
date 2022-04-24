import asyncio
import random

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import slash_command
from discord.ext import commands

parser = simdjson.Parser()


class waifuPics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="waifupics",
        description="Returns a random image of a waifu from waifu.pics",
    )
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
                waifu_pics = await r.content.read()
                waifu_pics_main = parser.parse(waifu_pics, recursive=True)
                try:
                    await ctx.respond(waifu_pics_main["url"])
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful"
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(waifuPics(bot))
