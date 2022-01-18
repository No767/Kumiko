import asyncio
import os

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Tenor_API_Key = os.getenv("Tenor_API_Key")


class TenorV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tenor-search-multiple", aliases=["tsm"])
    async def tenor_search(self, ctx, *, search: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": search,
                "key": Tenor_API_Key,
                "contentfilter": "medium",
                "limit": 5,
                "media_filter": "minimal",
            }
            async with session.get("https://g.tenor.com/v1/search", params=params) as r:
                data = await r.json()
                try:
                    embed1 = discord.Embed()
                    embed1.title = data["results"][0]["content_description"]
                    embed1.set_image(
                        url=data["results"][0]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed1)
                    embed2 = discord.Embed()
                    embed2.title = data["results"][1]["content_description"]
                    embed2.set_image(
                        url=data["results"][1]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed2)
                    embed3 = discord.Embed()
                    embed3.title = data["results"][2]["content_description"]
                    embed3.set_image(
                        url=data["results"][2]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed3)
                    embed4 = discord.Embed()
                    embed4.title = data["results"][3]["content_description"]
                    embed4.set_image(
                        url=data["results"][3]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed4)
                    embed5 = discord.Embed()
                    embed5.title = data["results"][4]["content_description"]
                    embed5.set_image(
                        url=data["results"][4]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed5)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = f"Sorry, but the search for {search} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @tenor_search.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tenor-search-one", aliases=["tso"])
    async def tenor_search_one(self, ctx, *, search_one: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": search_one,
                "key": Tenor_API_Key,
                "contentfilter": "medium",
                "limit": 2,
                "media_filter": "minimal",
            }
            async with session.get(
                "https://g.tenor.com/v1/search", params=params
            ) as re:
                data2 = await re.json()
                try:
                    embedVar1 = discord.Embed()
                    embedVar1.title = data2["results"][0]["content_description"]
                    embedVar1.set_image(
                        url=data2["results"][0]["media"][0]["gif"]["url"]
                    )
                    await ctx.send(embed=embedVar1)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "Sorry, but the search for {search} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @tenor_search_one.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tenor-trending", aliases=["tt"])
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
                data3 = await response.json()
                try:
                    embed1 = discord.Embed()
                    embed1.title = data3["results"][0]["content_description"]
                    embed1.set_image(
                        url=data3["results"][0]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed1)
                    embed2 = discord.Embed()
                    embed2.title = data3["results"][1]["content_description"]
                    embed2.set_image(
                        url=data3["results"][1]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed2)
                    embed3 = discord.Embed()
                    embed3.title = data3["results"][2]["content_description"]
                    embed3.set_image(
                        url=data3["results"][2]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed3)
                    embed4 = discord.Embed()
                    embed4.title = data3["results"][3]["content_description"]
                    embed4.set_image(
                        url=data3["results"][3]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed4)
                    embed5 = discord.Embed()
                    embed5.title = data3["results"][4]["content_description"]
                    embed5.set_image(
                        url=data3["results"][4]["media"][0]["gif"]["url"])
                    await ctx.send(embed=embed5)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "Sorry, but the search for {search} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tenor-search-suggestions", aliases=["tss"])
    async def tenor_search_suggestions(self, ctx, *, search_suggestion: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": Tenor_API_Key,
                      "q": search_suggestion, "limit": 25}
            async with session.get(
                "https://g.tenor.com/v1/search_suggestions", params=params
            ) as resp:
                data5 = await resp.json()
                try:
                    embedVar = discord.Embed()
                    embedVar.title = "Search Suggestions"
                    embedVar.description = str(
                        [items for items in data5["results"]]
                    ).replace("'", "")
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "Sorry, but the search for {search} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @tenor_search_suggestions.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tenor-trending-terms", aliases=["tt-terms"])
    async def tenor_trending_terms(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": Tenor_API_Key, "limit": 25}
            async with session.get(
                "https://g.tenor.com/v1/trending_terms", params=params
            ) as rep:
                data6 = await rep.json()
                try:
                    embedVar = discord.Embed()
                    embedVar.title = "Trending Search Terms"
                    embedVar.description = str(
                        [items for items in data6["results"]]
                    ).replace("'", "")
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "Sorry, but the search for {search} has failed. Please try again..."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @tenor_trending_terms.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV6(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tenor-gif", aliases=["tg"])
    async def tenor_gif(self, ctx, *, search_gif: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": Tenor_API_Key,
                "q": search_gif,
                "limit": 1,
                "media_filter": "minimal",
            }
            async with session.get(
                "https://g.tenor.com/v1/gifs", params=params
            ) as respon:
                data7 = await respon.json()
                try:
                    embedVar = discord.Embed()
                    embedVar.title = data7["results"][0]["content_description"]
                    embedVar.add_field(
                        name="GIF ID", value=data7["results"][0]["id"], inline=True
                    )
                    embedVar.add_field(
                        name="Item URL",
                        value=data7["results"][0]["itemurl"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Tags",
                        value=[items for items in data7["results"][0]["tags"]],
                        inline=True,
                    )
                    embedVar.add_field(
                        names="Flags",
                        value=[items for items in data7["results"][0]["flags"]],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Shares", value=data7["results"][0]["shares"], inline=True
                    )
                    embedVar.add_field(
                        name="Has Audio",
                        value=data7["results"][0]["has_audio"],
                        inline=True,
                    )
                    embedVar.set_image(
                        url=data7["results"][0]["media"][0]["gif"]["url"]
                    )
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "Sorry, but the query failed. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @tenor_gif.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TenorV7(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tenor-random", aliases=["tr"])
    async def tenor_random(self, ctx, *, search_random: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": Tenor_API_Key,
                "limit": 1,
                "media_filter": "minimal",
                "contentfilter": "medium",
                "q": search_random,
            }
            async with session.get(
                "https://g.tenor.com/v1/random", params=params
            ) as object:
                data8 = await object.json()
                try:
                    embedVar = discord.Embed()
                    embedVar.title = data8["results"][0]["content_description"]
                    embedVar.add_field(
                        name="GIF ID", value=data8["results"][0]["id"], inline=True
                    )
                    embedVar.add_field(
                        name="Item URL",
                        value=data8["results"][0]["itemurl"],
                        inline=True,
                    )
                    embedVar.set_image(
                        url=data8["results"][0]["media"][0]["gif"]["url"]
                    )
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "Sorry, but the query failed. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @tenor_random.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(TenorV1(bot))
    bot.add_cog(TenorV2(bot))
    bot.add_cog(TenorV3(bot))
    bot.add_cog(TenorV4(bot))
    bot.add_cog(TenorV5(bot))
    bot.add_cog(TenorV6(bot))
    bot.add_cog(TenorV7(bot))
