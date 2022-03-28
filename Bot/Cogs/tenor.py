import asyncio
import os

import aiohttp
import discord
import orjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Tenor_API_Key = os.getenv("Tenor_API_Key")


class TenorV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="tenor-search-multiple",
        description="Searches for up to 5 gifs on Tenor",
    )
    async def tenor_search(
        self, ctx, *, search_term: Option(str, "Search Term for GIFs")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": search_term,
                "key": Tenor_API_Key,
                "contentfilter": "medium",
                "limit": 5,
                "media_filter": "minimal",
            }
            async with session.get("https://g.tenor.com/v1/search", params=params) as r:
                data = await r.content.read()
                dataMain = orjson.loads(data)
                try:
                    embedVar = discord.Embed()
                    filterList = [
                        "created",
                        "bg_color",
                        "content_rating",
                        "title",
                        "h1_title",
                        "itemurl",
                        "url",
                        "shares",
                        "hasaudio",
                        "hascaption",
                        "source_id",
                        "composite",
                        "tags",
                        "flags",
                        "media",
                        "content_description",
                    ]
                    for dictItem in dataMain["results"]:
                        for key in dictItem.items():
                            if key not in filterList:
                                embedVar.title = dictItem["content_description"]
                        for item in dictItem.get("media"):
                            embedVar.set_image(url=item["gif"]["url"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = f"Sorry, but the search for {search_term} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="tenor-search-one",
        description="Searches for a single gif on Tenor",
    )
    async def tenor_search_one(
        self, ctx, *, search_one_term: Option(str, "Search Term for GIF")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": search_one_term,
                "key": Tenor_API_Key,
                "contentfilter": "medium",
                "limit": 1,
                "media_filter": "minimal",
            }
            async with session.get(
                "https://g.tenor.com/v1/search", params=params
            ) as re:
                data2 = await re.content.read()
                dataMain2 = orjson.loads(data2)
                try:
                    embedVar1 = discord.Embed()
                    embedVar1.title = dataMain2["results"][0]["content_description"]
                    embedVar1.set_image(
                        url=dataMain2["results"][0]["media"][0]["gif"]["url"]
                    )
                    await ctx.send(embed=embedVar1)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = f"Sorry, but the search for {search_one_term} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="tenor-trending",
        description="Returns up to 5 trending gifs from Tenor",
    )
    async def tenor_trending(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": Tenor_API_Key,
                "contentfilter": "medium",
                "limit": 5,
                "media_filter": "minimal",
            }
            async with session.get(
                "https://g.tenor.com/v1/trending", params=params
            ) as response:
                data3 = await response.content.read()
                dataMain3 = orjson.loads(data3)
                try:
                    embedVar = discord.Embed()
                    filterList2 = [
                        "created",
                        "bg_color",
                        "content_rating",
                        "title",
                        "h1_title",
                        "itemurl",
                        "url",
                        "shares",
                        "hasaudio",
                        "hascaption",
                        "source_id",
                        "composite",
                        "tags",
                        "flags",
                        "media",
                        "content_description",
                    ]
                    for dictItem2 in dataMain3["results"]:
                        for key in dictItem2.items():
                            if key not in filterList2:
                                embedVar.title = dictItem2["content_description"]
                        for item2 in dictItem2.get("media"):
                            embedVar.set_image(url=item2["gif"]["url"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "Sorry, but the query has failed. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="tenor-search-suggestions",
        description="Gives a list of suggested search terms based on given topic",
    )
    async def tenor_search_suggestions(
        self,
        ctx,
        *,
        search_suggestion: Option(str, "Topic/Search Term for Search Suggestion"),
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": Tenor_API_Key,
                      "q": search_suggestion, "limit": 25}
            async with session.get(
                "https://g.tenor.com/v1/search_suggestions", params=params
            ) as resp:
                data5 = await resp.content.read()
                dataMain5 = orjson.loads(data5)
                try:
                    embedVar = discord.Embed()
                    embedVar.title = "Search Suggestions"
                    embedVar.description = str(
                        [items for items in dataMain5["results"]]
                    ).replace("'", "")
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "Sorry, but the search for {search} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="tenor-trending-terms",
        description="Gives a list of trending search terms on Tenor",
    )
    async def tenor_trending_terms(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": Tenor_API_Key, "limit": 25}
            async with session.get(
                "https://g.tenor.com/v1/trending_terms", params=params
            ) as rep:
                data6 = await rep.content.read()
                dataMain6 = orjson.loads(data6)
                try:
                    embedVar = discord.Embed()
                    embedVar.title = "Trending Search Terms"
                    embedVar.description = str(
                        [items for items in dataMain6["results"]]
                    ).replace("'", "")
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "Sorry, but the search for {search} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV6(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="tenor-gif",
        description="Gives a gif based on the given GIF ID",
    )
    async def tenor_gif(self, ctx, *, search_gif: Option(int, "Tenor GIF ID")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": Tenor_API_Key,
                "ids": search_gif,
                "limit": 1,
                "media_filter": "minimal",
            }
            async with session.get(
                "https://g.tenor.com/v1/gifs", params=params
            ) as respon:
                data7 = await respon.content.read()
                dataMain7 = orjson.loads(data7)
                try:
                    embedVar = discord.Embed()
                    filterList2 = [
                        "created",
                        "bg_color",
                        "content_rating",
                        "title",
                        "h1_title",
                        "url",
                        "hasaudio",
                        "hascaption",
                        "source_id",
                        "composite",
                        "media",
                        "tags",
                        "flags",
                        "content_description",
                        "shares",
                    ]
                    for dictValues in dataMain7["results"]:
                        for k, v in dictValues.items():
                            if k not in filterList2:
                                embedVar.title = dictValues["content_description"]
                                embedVar.add_field(
                                    name=str(k).capitalize(), value=v, inline=True
                                )
                        for item3 in dictValues.get("media"):
                            embedVar.set_image(url=item3["gif"]["url"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "Sorry, but the query failed. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV7(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="tenor-random",
        description="Gives a random gif from Tenor based on given search term",
    )
    async def tenor_random(
        self, ctx, *, search_random_term: Option(str, "Search Term")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": Tenor_API_Key,
                "limit": 5,
                "media_filter": "minimal",
                "contentfilter": "medium",
                "q": search_random_term,
            }
            async with session.get(
                "https://g.tenor.com/v1/random", params=params
            ) as object3:
                data8 = await object3.content.read()
                dataMain8 = orjson.loads(data8)
                try:
                    embedVar = discord.Embed()
                    for dict_items in dataMain8["results"]:
                        for _ in dict_items.items():
                            embedVar.title = dict_items["content_description"]
                        for item3 in dict_items.get("media"):
                            embedVar.set_image(url=item3["gif"]["url"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "Sorry, but the query failed. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(TenorV1(bot))
    bot.add_cog(TenorV2(bot))
    bot.add_cog(TenorV3(bot))
    bot.add_cog(TenorV4(bot))
    bot.add_cog(TenorV5(bot))
    bot.add_cog(TenorV6(bot))
    bot.add_cog(TenorV7(bot))
