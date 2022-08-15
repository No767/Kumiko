import asyncio
import os
import re

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
from rin_exceptions import SusEveryonePing

load_dotenv()

KUMIKO_TENOR_API_KEY = os.getenv("Kumiko_Tenor_API_Key")

parser = simdjson.Parser()


class UwU(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    uwu = SlashCommandGroup("uwu", "uwu", guild_ids=[970159505390325842])

    @uwu.command(name="cuddle")
    async def getAnimeCuddle(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """Cuddle with someone...."""
        try:
            try:
                if username in ["@everyone", "@here"]:
                    raise SusEveryonePing
                else:
                    requestedUserID = int(re.sub("[^a-zA-Z0-9 ]", "", username))
                    getUserInfo = await self.bot.get_or_fetch_user(requestedUserID)
                    randomList = []
                    async with aiohttp.ClientSession(
                        json_serialize=orjson.dumps
                    ) as session:
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
                            for items in dataMain["results"]:
                                randomList.append(items["media_formats"]["gif"]["url"])
                            rng = default_rng()
                            randArray = np.array(randomList)
                            embed = discord.Embed()
                            embed.title = f"{ctx.user.display_name} cuddles {getUserInfo.display_name} ! cuteeeeeee !"
                            embed.set_author(
                                name=ctx.user.display_name,
                                icon_url=ctx.user.display_avatar.url,
                            )
                            embed.set_image(url=rng.choice(randArray))

                            await ctx.respond(embed=embed)
            except SusEveryonePing:
                embedSus = discord.Embed()
                embedSus.description = (
                    "LMAO hahahahahahahhah you can't ping everyone like that..."
                )
                await ctx.respond(embed=embedSus)
        except ValueError:
            embedError = discord.Embed()
            embedError.description = "It seems like you entered in the actual username of the user. Make sure to input the actual user with the @ symbol in front (as if you were pinging them)"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="hug")
    async def getAnimeHug(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """Hug with someone...."""
        try:
            try:
                if username in ["@everyone", "@here"]:
                    raise SusEveryonePing
                else:
                    requestedUserID = int(re.sub("[^a-zA-Z0-9 ]", "", username))
                    getUserInfo = await self.bot.get_or_fetch_user(requestedUserID)
                    randomList = []
                    async with aiohttp.ClientSession(
                        json_serialize=orjson.dumps
                    ) as session:
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
                            for items in dataMain["results"]:
                                randomList.append(items["media_formats"]["gif"]["url"])
                            rng = default_rng()
                            randArray = np.array(randomList)
                            embed = discord.Embed()
                            embed.title = f"{ctx.user.display_name} hugs {getUserInfo.display_name} !"
                            embed.set_author(
                                name=ctx.user.display_name,
                                icon_url=ctx.user.display_avatar.url,
                            )
                            embed.set_image(url=rng.choice(randArray))
                            await ctx.respond(embed=embed)

            except SusEveryonePing:
                embedSus = discord.Embed()
                embedSus.description = (
                    "LMAO hahahahahahahhah you can't ping everyone like that..."
                )
                await ctx.respond(embed=embedSus)
        except ValueError:
            embedError = discord.Embed()
            embedError.description = "It seems like you entered in the actual username of the user. Make sure to input the actual user with the @ symbol in front (as if you were pinging them)"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="kiss")
    async def getAnimeKiss(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """awww u just kissed someone"""
        try:
            try:
                if username in ["@everyone", "@here"]:
                    raise SusEveryonePing
                else:
                    requestedUserID = int(re.sub("[^a-zA-Z0-9 ]", "", username))
                    getUserInfo = await self.bot.get_or_fetch_user(requestedUserID)
                    randomList = []
                    async with aiohttp.ClientSession(
                        json_serialize=orjson.dumps
                    ) as session:
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
                            for items in dataMain["results"]:
                                randomList.append(items["media_formats"]["gif"]["url"])
                            rng = default_rng()
                            randArray = np.array(randomList)
                            embed = discord.Embed()
                            embed.title = f"{ctx.user.display_name} kissed {getUserInfo.display_name} !"
                            embed.set_author(
                                name=ctx.user.display_name,
                                icon_url=ctx.user.display_avatar.url,
                            )
                            embed.set_image(url=rng.choice(randArray))
                            await ctx.respond(embed=embed)
            except SusEveryonePing:
                embedSus = discord.Embed()
                embedSus.description = (
                    "LMAO hahahahahahahhah you can't ping everyone like that..."
                )
                await ctx.respond(embed=embedSus)
        except ValueError:
            embedError = discord.Embed()
            embedError.description = "It seems like you entered in the actual username of the user. Make sure to input the actual user with the @ symbol in front (as if you were pinging them)"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="blushes")
    async def getAnimeBlush(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """blushes"""
        try:
            try:
                if username in ["@everyone", "@here"]:
                    raise SusEveryonePing
                else:
                    requestedUserID = int(re.sub("[^a-zA-Z0-9 ]", "", username))
                    getUserInfo = await self.bot.get_or_fetch_user(requestedUserID)
                    randomList = []
                    async with aiohttp.ClientSession(
                        json_serialize=orjson.dumps
                    ) as session:
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
                            for items in dataMain["results"]:
                                randomList.append(items["media_formats"]["gif"]["url"])
                            rng = default_rng()
                            randArray = np.array(randomList)
                            embed = discord.Embed()
                            embed.title = f"{ctx.user.display_name} made {getUserInfo.display_name} blush !"
                            embed.set_author(
                                name=ctx.user.display_name,
                                icon_url=ctx.user.display_avatar.url,
                            )
                            embed.set_image(url=rng.choice(randArray))
                            await ctx.respond(embed=embed)
            except SusEveryonePing:
                embedSus = discord.Embed()
                embedSus.description = (
                    "LMAO hahahahahahahhah you can't ping everyone like that..."
                )
                await ctx.respond(embed=embedSus)
        except ValueError:
            embedError = discord.Embed()
            embedError.description = "It seems like you entered in the actual username of the user. Make sure to input the actual user with the @ symbol in front (as if you were pinging them)"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="pout")
    async def getAnimePout(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """Makes the user kinda um pout in a cute way"""
        try:
            try:
                if username in ["@everyone", "@here"]:
                    raise SusEveryonePing
                else:
                    requestedUserID = int(re.sub("[^a-zA-Z0-9 ]", "", username))
                    getUserInfo = await self.bot.get_or_fetch_user(requestedUserID)
                    randomList = []
                    async with aiohttp.ClientSession(
                        json_serialize=orjson.dumps
                    ) as session:
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
                            for items in dataMain["results"]:
                                randomList.append(items["media_formats"]["gif"]["url"])
                            rng = default_rng()
                            randArray = np.array(randomList)
                            embed = discord.Embed()
                            embed.title = f"{ctx.user.display_name} made {getUserInfo.display_name} pout !"
                            embed.set_author(
                                name=ctx.user.display_name,
                                icon_url=ctx.user.display_avatar.url,
                            )
                            embed.set_image(url=rng.choice(randArray))
                            await ctx.respond(embed=embed)
            except SusEveryonePing:
                embedSus = discord.Embed()
                embedSus.description = (
                    "LMAO hahahahahahahhah you can't ping everyone like that..."
                )
                await ctx.respond(embed=embedSus)
        except ValueError:
            embedError = discord.Embed()
            embedError.description = "It seems like you entered in the actual username of the user. Make sure to input the actual user with the @ symbol in front (as if you were pinging them)"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="tickle")
    async def getAnimeTickle(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """Tickles the user uwu"""
        try:
            try:
                if username in ["@everyone", "@here"]:
                    raise SusEveryonePing
                else:
                    requestedUserID = int(re.sub("[^a-zA-Z0-9 ]", "", username))
                    getUserInfo = await self.bot.get_or_fetch_user(requestedUserID)
                    randomList = []
                    async with aiohttp.ClientSession(
                        json_serialize=orjson.dumps
                    ) as session:
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
                            for items in dataMain["results"]:
                                randomList.append(items["media_formats"]["gif"]["url"])
                            rng = default_rng()
                            randArray = np.array(randomList)
                            embed = discord.Embed()
                            embed.title = f"{ctx.user.display_name} tickled {getUserInfo.display_name} !"
                            embed.set_author(
                                name=ctx.user.display_name,
                                icon_url=ctx.user.display_avatar.url,
                            )
                            embed.set_image(url=rng.choice(randArray))
                            await ctx.respond(embed=embed)
            except SusEveryonePing:
                embedSus = discord.Embed()
                embedSus.description = (
                    "LMAO hahahahahahahhah you can't ping everyone like that..."
                )
                await ctx.respond(embed=embedSus)
        except ValueError:
            embedError = discord.Embed()
            embedError.description = "It seems like you entered in the actual username of the user. Make sure to input the actual user with the @ symbol in front (as if you were pinging them)"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @uwu.command(name="headpat")
    async def getAnimeHeadpat(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """Gives a headpat to the user"""
        try:
            try:
                if username in ["@everyone", "@here"]:
                    raise SusEveryonePing
                else:
                    requestedUserID = int(re.sub("[^a-zA-Z0-9 ]", "", username))
                    getUserInfo = await self.bot.get_or_fetch_user(requestedUserID)
                    randomList = []
                    async with aiohttp.ClientSession(
                        json_serialize=orjson.dumps
                    ) as session:
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
                            for items in dataMain["results"]:
                                randomList.append(items["media_formats"]["gif"]["url"])
                            rng = default_rng()
                            randArray = np.array(randomList)
                            embed = discord.Embed()
                            embed.title = f"{ctx.user.display_name} gave {getUserInfo.display_name} a headpat!"
                            embed.set_author(
                                name=ctx.user.display_name,
                                icon_url=ctx.user.display_avatar.url,
                            )
                            embed.set_image(url=rng.choice(randArray))
                            await ctx.respond(embed=embed)
            except SusEveryonePing:
                embedSus = discord.Embed()
                embedSus.description = (
                    "LMAO hahahahahahahhah you can't ping everyone like that..."
                )
                await ctx.respond(embed=embedSus)
        except ValueError:
            embedError = discord.Embed()
            embedError.description = "It seems like you entered in the actual username of the user. Make sure to input the actual user with the @ symbol in front (as if you were pinging them)"
            await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(UwU(bot))
