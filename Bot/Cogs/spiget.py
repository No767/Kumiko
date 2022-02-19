import asyncio

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands
from discord.commands import slash_command, Option


class SpigetV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="spiget-search", description="Finds up to 5 plugins matching the name of the given plugin", guild_ids=[866199405090308116])
    async def spigetSearch(self, ctx, *, plugin_name: Option(str, "The name of the plugin")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"User-Agent": "Mozilla/5.0"}
            params = {"size": 5}
            async with session.get(
                f"https://api.spiget.org/v2/search/resources/{plugin_name}", headers=headers, params=params
            ) as r:
                resource = await r.json()
                try:
                    for dictItem in resource:
                        thumbnail = (
                            "https://www.spigotmc.org/" +
                            dictItem["icon"]["url"]
                        )
                        download_url_external_false = "https://spigotmc.org/" + str(
                            dictItem["file"]["url"]
                        )
                        filter = [
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
                        if dictItem["file"]["type"] in "external":
                            embedVar = discord.Embed(
                                title=dictItem["name"],
                                color=discord.Color.from_rgb(173, 156, 255),
                            )
                            embedVar.description = dictItem["tag"]
                            for key, value in dictItem.items():
                                if key not in filter:
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
                                        name=k, value=v, inline=True)
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
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = (
                        "The query failed. Please Try Again...."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class SpigetV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name="spiget-author", description="Returns some info about a plugin author", guild_ids=[866199405090308116])
    async def spigetAuthor(self, ctx, *, author_name: Option(str, "Name of the plugin author")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"User-Agent": "Mozilla/5.0"}
            params = {"size": 5}
            async with session.get(f"https://api.spiget.org/v2/search/authors/{author_name}", headers=headers, params=params) as r:
                data = await r.json()
                authorFilter = ["icon", "name", "identities"]
                embedVar = discord.Embed()
                try:
                    for dictItem in data:
                        embedVar.title = dictItem["name"]
                        embedVar.set_thumbnail(url=dictItem["icon"]["url"])
                        for k, v in dictItem.items():
                            if k not in authorFilter:
                                embedVar.add_field(name=k, value=v, inline=True)
                        for keys, value in dictItem["identities"].items():
                            embedVar.add_field(name=keys, value=value, inline=True)
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar.description = "The query failed. Please Try Again...."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

class SpigetV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="spiget-stats", description="Returns stats for SpigotMC", guild_ids=[866199405090308116])
    async def spigetStats(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"User-Agent": "Mozilla/5.0"}
            async with session.get(
                "https://api.spiget.org/v2/status", headers=headers
            ) as res:
                total_stats = await res.json()
                try:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    for key, val in total_stats["stats"].items():
                        embedVar.add_field(name=key, value=val, inline=True)

                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = (
                        "The query failed. Please Try Again"
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class SpigetV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="spiget-status", description="Returns the status of Spiget (HTTP Status)", guild_ids=[866199405090308116])
    async def spigetStatus(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"User-Agent": "Mozilla/5.0"}
            async with session.get(
                "https://api.spiget.org/v2/status", headers=headers
            ) as r:
                try:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.add_field(
                        name="Status", value=r.status, inline=True)
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = (
                        "The query failed. Please Try Again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(SpigetV2(bot))
    bot.add_cog(SpigetV3(bot))
    bot.add_cog(SpigetV4(bot))
    bot.add_cog(SpigetV5(bot))
