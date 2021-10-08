import json
import os
import random

import discord
import requests
from discord import Embed
from discord.ext import commands


def anime_pics(waifu_list):
    link = f"https://api.waifu.pics/sfw/{waifu_list}"
    r = requests.get(link)
    anime_data = r.text
    waifu = json.loads(anime_data)
    return waifu


def waifu_picker():
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
    return searchterm


class waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="waifupics")
    async def on_messsage(self, ctx):
        waifu_search = waifu_picker()
        waifu_pics = anime_pics(waifu_search)
        try:
            await ctx.send(waifu_pics["url"])
        except:
            embedVar = discord.Embed()
            embedVar.description = f"""
            The query was not successful.
            """
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(waifu(bot))
