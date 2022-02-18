import asyncio

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands


class SpigetV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spiget-search")
    async def spigetSearch(self, ctx, *, search: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"User-Agent": "Mozilla/5.0"}
            async with session.get(
                f"https://api.spiget.org/v2/search/resources/{search}", headers=headers
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
                        filter = ["icon", "links", "releaseDate", "updateDate", "category", "author",
                                  "version", "id", "external", "tag", "rating", "existenceStatus", "name", "file"]
                        itemFilter = ["url"]
                        if dictItem["file"]["type"] in "external":
                            embedVar = discord.Embed(
                                title=resource[0]["name"],
                                color=discord.Color.from_rgb(
                                    173, 156, 255),
                            )
                            embedVar.description = dictItem["tag"]
                            for key, value in dictItem.items():
                                if key not in filter:
                                    embedVar.add_field(name=key, value=value, inline=True)
                            for item1, res1 in dictItem["file"].items():
                                if item1 not in itemFilter:
                                    embedVar.add_field(name=item1, value=f"{[res1]}".replace("'", ""), inline=True)
                            embedVar.add_field(name="Rating", value=dictItem["rating"]["average"], inline=True)
                            embedVar.set_thumbnail(url=str(thumbnail))
                            await ctx.send(embed=embedVar)
                        else:
                            embedVar = discord.Embed(
                                title=resource[0]["name"],
                                color=discord.Color.from_rgb(
                                    173, 156, 255),
                            )
                            embedVar.description = dictItem["tag"] 
                            for k, v in dictItem.items():
                                if k not in filter:
                                    embedVar.add_field(name=k, value=v, inline=True)
                            for item, res in dictItem["file"].items():
                                if item not in itemFilter:
                                    embedVar.add_field(name=item, value=f"{[res]}".replace("'", ""), inline=True)
                            embedVar.add_field(name="Rating", value=dictItem["rating"]["average"], inline=True)
                            embedVar.add_field(
                                name="Download URL",
                                value=f"{download_url_external_false}",
                                inline=False,
                            )
                            embedVar.set_thumbnail(url=str(thumbnail))
                            await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = (
                        f"The query failed. Please Try Again.\nReason: {e}"
                    )
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @spigetSearch.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = "Missing a required argument: Plugin Name\n\nFor selecting a plugin, the name must be the exact as the one from Spigot. So for example, if I wanted to search up FastAsyncWorldEdit (FAWE), I would put `Fast Async WorldEdit`"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class SpigetV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spiget-stats")
    async def on_message(self, ctx):
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

                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = (
                        f"The query failed. Please Try Again.\nReason: {e}"
                    )
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class SpigetV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spiget-status")
    async def on_message(self, ctx):
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
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(173, 156, 255)
                    )
                    embedVar.description = (
                        f"The query failed. Please Try Again.\nReason: {e}"
                    )
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(SpigetV2(bot))
    bot.add_cog(SpigetV4(bot))
    bot.add_cog(SpigetV5(bot))
