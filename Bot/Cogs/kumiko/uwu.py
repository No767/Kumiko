import asyncio
import os

import aiohttp
import discord
import numpy as np
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from numpy.random import default_rng
from rin_exceptions import NoItemsError

load_dotenv()

KUMIKO_TENOR_API_KEY = os.getenv("Kumiko_Tenor_API_Key")

parser = simdjson.Parser()


class UwU(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    uwu = SlashCommandGroup("uwu", "uwu", guild_ids=[970159505390325842])

    @uwu.command(name="cuddle")
    async def getAnimeCuddle(
        self, ctx, *, username: Option(discord.Member, "The username of the user")
    ):
        """Cuddle with someone...."""
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                params = {
                    "key": KUMIKO_TENOR_API_KEY,
                    "limit": 50,
                    "q": "cute anime cuddles",
                    "random": "true",
                }
                async with session.get(
                    "https://tenor.googleapis.com/v2/search", params=params
                ) as r:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    randomList = []
                    if len(dataMain["results"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        for items in dataMain["results"]:
                            randomList.append(items["media_formats"]["gif"]["url"])
                        rng = default_rng()
                        randArray = np.array(randomList)
                        embed = discord.Embed()
                        embed.title = f"{ctx.user.display_name} cuddles {username.display_name} ! cuteeeeeee !"
                        embed.set_author(
                            name=ctx.user.display_name,
                            icon_url=ctx.user.display_avatar.url,
                        )
                        embed.set_image(url=rng.choice(randArray))
                        await ctx.respond(embed=embed)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                "Oops there seems to be no results for that... sorry"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="hug")
    async def getAnimeHug(
        self, ctx, *, username: Option(discord.Member, "The username of the user")
    ):
        """Hug with someone...."""
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                params = {
                    "key": KUMIKO_TENOR_API_KEY,
                    "limit": 50,
                    "q": "cute anime hug",
                    "random": "true",
                }
                async with session.get(
                    "https://tenor.googleapis.com/v2/search", params=params
                ) as r:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    randomList = []
                    if len(dataMain["results"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        for items in dataMain["results"]:
                            randomList.append(items["media_formats"]["gif"]["url"])
                        rng = default_rng()
                        randArray = np.array(randomList)
                        embed = discord.Embed()
                        embed.title = (
                            f"{ctx.user.display_name} hugs {username.display_name} !"
                        )
                        embed.set_author(
                            name=ctx.user.display_name,
                            icon_url=ctx.user.display_avatar.url,
                        )
                        embed.set_image(url=rng.choice(randArray))
                        await ctx.respond(embed=embed)

        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                "Oops there seems to be no results for that... sorry"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="kiss")
    async def getAnimeKiss(
        self, ctx, *, username: Option(discord.Member, "The username of the user")
    ):
        """awww u just kissed someone"""
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                params = {
                    "key": KUMIKO_TENOR_API_KEY,
                    "limit": 50,
                    "q": "cute anime kiss",
                    "random": "true",
                }
                async with session.get(
                    "https://tenor.googleapis.com/v2/search", params=params
                ) as r:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    randomList = []
                    if len(dataMain["results"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        for items in dataMain["results"]:
                            randomList.append(items["media_formats"]["gif"]["url"])
                        rng = default_rng()
                        randArray = np.array(randomList)
                        embed = discord.Embed()
                        embed.title = (
                            f"{ctx.user.display_name} kissed {username.display_name} !"
                        )
                        embed.set_author(
                            name=ctx.user.display_name,
                            icon_url=ctx.user.display_avatar.url,
                        )
                        embed.set_image(url=rng.choice(randArray))
                        await ctx.respond(embed=embed)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                "Oops there seems to be no results for that... sorry"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="blushes")
    async def getAnimeBlush(
        self, ctx, *, username: Option(discord.Member, "The username of the user")
    ):
        """blushes"""
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                params = {
                    "key": KUMIKO_TENOR_API_KEY,
                    "limit": 50,
                    "q": "cute anime blush",
                    "random": "true",
                }
                async with session.get(
                    "https://tenor.googleapis.com/v2/search", params=params
                ) as r:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    randomList = []
                    if len(dataMain["results"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        for items in dataMain["results"]:
                            randomList.append(items["media_formats"]["gif"]["url"])
                        rng = default_rng()
                        randArray = np.array(randomList)
                        embed = discord.Embed()
                        embed.title = f"{ctx.user.display_name} made {username.display_name} blush !"
                        embed.set_author(
                            name=ctx.user.display_name,
                            icon_url=ctx.user.display_avatar.url,
                        )
                        embed.set_image(url=rng.choice(randArray))
                        await ctx.respond(embed=embed)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                "Oops there seems to be no results for that... sorry"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="pout")
    async def getAnimePout(
        self, ctx, *, username: Option(discord.Member, "The username of the user")
    ):
        """Makes the user kinda um pout in a cute way"""
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                params = {
                    "key": KUMIKO_TENOR_API_KEY,
                    "limit": 50,
                    "q": "cute anime pout",
                    "random": "true",
                }
                async with session.get(
                    "https://tenor.googleapis.com/v2/search", params=params
                ) as r:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    randomList = []
                    if len(dataMain["results"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        for items in dataMain["results"]:
                            randomList.append(items["media_formats"]["gif"]["url"])
                        rng = default_rng()
                        randArray = np.array(randomList)
                        embed = discord.Embed()
                        embed.title = f"{ctx.user.display_name} made {username.display_name} pout !"
                        embed.set_author(
                            name=ctx.user.display_name,
                            icon_url=ctx.user.display_avatar.url,
                        )
                        embed.set_image(url=rng.choice(randArray))
                        await ctx.respond(embed=embed)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                "Oops there seems to be no results for that... sorry"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="tickle")
    async def getAnimeTickle(
        self, ctx, *, username: Option(discord.Member, "The username of the user")
    ):
        """Tickles the user uwu"""
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                params = {
                    "key": KUMIKO_TENOR_API_KEY,
                    "limit": 50,
                    "q": "cute anime tickle",
                    "random": "true",
                }
                async with session.get(
                    "https://tenor.googleapis.com/v2/search", params=params
                ) as r:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    randomList = []
                    if len(dataMain["results"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        for items in dataMain["results"]:
                            randomList.append(items["media_formats"]["gif"]["url"])
                        rng = default_rng()
                        randArray = np.array(randomList)
                        embed = discord.Embed()
                        embed.title = (
                            f"{ctx.user.display_name} tickled {username.display_name} !"
                        )
                        embed.set_author(
                            name=ctx.user.display_name,
                            icon_url=ctx.user.display_avatar.url,
                        )
                        embed.set_image(url=rng.choice(randArray))
                        await ctx.respond(embed=embed)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                "Oops there seems to be no results for that... sorry"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="headpat")
    async def getAnimeHeadpat(
        self, ctx, *, username: Option(discord.Member, "The username of the user")
    ):
        """Gives a headpat to the user"""
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                params = {
                    "key": KUMIKO_TENOR_API_KEY,
                    "limit": 50,
                    "q": "cute anime headpat",
                    "random": "true",
                }
                async with session.get(
                    "https://tenor.googleapis.com/v2/search", params=params
                ) as r:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    randomList = []
                    if len(dataMain["results"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        for items in dataMain["results"]:
                            randomList.append(items["media_formats"]["gif"]["url"])
                        rng = default_rng()
                        randArray = np.array(randomList)
                        embed = discord.Embed()
                        embed.title = f"{ctx.user.display_name} gave {username.display_name} a headpat!"
                        embed.set_author(
                            name=ctx.user.display_name,
                            icon_url=ctx.user.display_avatar.url,
                        )
                        embed.set_image(url=rng.choice(randArray))
                        await ctx.respond(embed=embed)
        except NoItemsError:
            embedError = discord.Embed()
            embedError.description = (
                "Oops there seems to be no results for that... sorry"
            )
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(UwU(bot))
