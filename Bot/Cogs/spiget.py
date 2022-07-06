import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands

parser = simdjson.Parser()


class SpigetV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    spiget = SlashCommandGroup("spigot", "Commands for Spiget")

    @spiget.command(name="search")
    async def spigetSearch(
        self, ctx, *, plugin_name: Option(str, "The name of the plugin")
    ):
        """Finds up to 5 plugins matching the name of the given plugin"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
            }
            params = {"size": 5}
            async with session.get(
                f"https://api.spiget.org/v2/search/resources/{plugin_name}",
                headers=headers,
                params=params,
            ) as r:
                resource = await r.content.read()
                try:
                    resourceMain = parser.parse(resource, recursive=True)
                    try:
                        if len(resourceMain) == 0:
                            raise ValueError
                        else:
                            for dictItem in resourceMain:
                                thumbnail = (
                                    "https://www.spigotmc.org/"
                                    + dictItem["icon"]["url"]
                                )
                                download_url_external_false = (
                                    "https://spigotmc.org/"
                                    + str(dictItem["file"]["url"])
                                )
                                filterMain6 = [
                                    "icon",
                                    "links",
                                    "releaseDate",
                                    "updateDate",
                                    "category",
                                    "author",
                                    "version",
                                    "id",
                                    "external",
                                    "tag",
                                    "rating",
                                    "existenceStatus",
                                    "name",
                                    "file",
                                ]
                                itemFilter = ["url"]
                                for dictItemMain in resourceMain:
                                    if not dictItemMain["external"]:
                                        embedVar = discord.Embed(
                                            title=dictItem["name"],
                                            color=discord.Color.from_rgb(173, 156, 255),
                                        )
                                        embedVar.description = dictItem["tag"]
                                        for key, value in dictItem.items():
                                            if key not in filterMain6:
                                                embedVar.add_field(
                                                    name=key, value=value, inline=True
                                                )
                                        for item1, res1 in dictItem["file"].items():
                                            if item1 not in itemFilter:
                                                embedVar.add_field(
                                                    name=item1,
                                                    value=f"{[res1]}".replace("'", ""),
                                                    inline=True,
                                                )
                                        embedVar.add_field(
                                            name="Rating",
                                            value=dictItem["rating"]["average"],
                                            inline=True,
                                        )
                                        embedVar.set_thumbnail(url=str(thumbnail))
                                        await ctx.respond(embed=embedVar)
                                    else:
                                        embedVar = discord.Embed(
                                            title=dictItem["name"],
                                            color=discord.Color.from_rgb(173, 156, 255),
                                        )
                                        embedVar.description = dictItem["tag"]
                                        for k, v in dictItem.items():
                                            if k not in filter:
                                                embedVar.add_field(
                                                    name=k, value=v, inline=True
                                                )
                                        for item, res in dictItem["file"].items():
                                            if item not in itemFilter:
                                                embedVar.add_field(
                                                    name=item,
                                                    value=f"{[res]}".replace("'", ""),
                                                    inline=True,
                                                )
                                        embedVar.add_field(
                                            name="Rating",
                                            value=dictItem["rating"]["average"],
                                            inline=True,
                                        )
                                        embedVar.add_field(
                                            name="Download URL",
                                            value=f"{download_url_external_false}",
                                            inline=False,
                                        )
                                        embedVar.set_thumbnail(url=str(thumbnail))
                                        await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedErrorMain = discord.Embed()
                        embedErrorMain.description = (
                            "No results found... Please try again"
                        )
                        await ctx.respond(embed=embedErrorMain)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = "The query failed. Please Try Again...."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @spiget.command(name="author")
    async def spigetAuthor(
        self, ctx, *, author_name: Option(str, "Name of the plugin author")
    ):
        """Returns some info about a plugin author"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
            }
            params = {"size": 5}
            async with session.get(
                f"https://api.spiget.org/v2/search/authors/{author_name}",
                headers=headers,
                params=params,
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    authorFilter = ["icon", "name", "identities"]
                    embedVar = discord.Embed()

                    try:
                        if len(dataMain) == 0:
                            raise ValueError
                        else:
                            for dictItem in dataMain:
                                embedVar.title = dictItem["name"]
                                embedVar.set_thumbnail(url=dictItem["icon"]["url"])
                                for k, v in dictItem.items():
                                    if k not in authorFilter:
                                        embedVar.add_field(name=k, value=v, inline=True)
                                for keys, value in dictItem["identities"].items():
                                    embedVar.add_field(
                                        name=keys, value=value, inline=True
                                    )
                                await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedValueError = discord.Embed()
                        embedValueError.description = f"It seems like there were no authors named {author_name}... Please try again"
                        await ctx.respond(embed=embedValueError)
                except Exception as e:
                    embedExceptionError = discord.Embed()
                    embedExceptionError.description = (
                        "The query failed. Please Try Again...."
                    )
                    embedExceptionError.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedExceptionError)

    @spiget.command(name="stats")
    async def spigetStats(self, ctx):
        """Returns stats for SpigotMC"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
            }
            async with session.get(
                "https://api.spiget.org/v2/status", headers=headers
            ) as res:
                total_stats = await res.content.read()
                totalStatsMain = parser.parse(total_stats, recursive=True)
                try:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    for key, val in totalStatsMain["stats"].items():
                        embedVar.add_field(name=key, value=val, inline=True)

                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = "The query failed. Please Try Again"
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @spiget.command(name="status")
    async def spigetStatus(self, ctx):
        """Returns the status of Spigot (HTTP Status)"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
            }
            async with session.get(
                "https://api.spiget.org/v2/status", headers=headers
            ) as r:
                try:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.add_field(name="Status", value=r.status, inline=True)
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = "The query failed. Please Try Again."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(SpigetV1(bot))
