import random

import discord
import requests
import ujson
from discord.ext import commands


def anime_pics():
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
    link = f"https://api.waifu.pics/sfw/{searchterm}"
    r = requests.get(link)
    return ujson.loads(r.text)


class waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="waifupics")
    async def on_messsage(self, ctx):
        waifu_pics = anime_pics()
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
