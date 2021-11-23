import random

import discord
import ujson
from discord.ext import commands
import aiohttp

class waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="waifupics")
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
        async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
            async with session.get(f"https://api.waifu.pics/sfw/{searchterm}") as r:
                waifu_pics = await r.json()
                try:
                    await ctx.send(waifu_pics["url"])
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = f"""
                    The query was not successful.\nReason: {e}
                    """
                    await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(waifu(bot))
