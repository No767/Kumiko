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
                author_id = resource[0]["author"]["id"]
                resource_id = resource[0]["id"]
                async with session.get(
                    f"https://api.spiget.org/v2/authors/{author_id}", headers=headers
                ) as resp:
                    author_details_v1 = await resp.json()
                    async with session.get(
                        f"https://api.spiget.org/v2/resources/{resource_id}/versions",
                        headers=headers,
                    ) as response:
                        spigetv3 = await response.json()
                        async with session.get(
                            f"https://api.spiget.org/v2/resources/{resource_id}/versions/latest",
                            headers=headers,
                        ) as another_response:
                            plugin_version = await another_response.json()
                            thumbnail = (
                                "https://www.spigotmc.org/" +
                                resource[0]["icon"]["url"]
                            )
                            file_size = str(resource[0]["file"]["size"]) + str(
                                resource[0]["file"]["sizeUnit"]
                            )
                            download_url_external_false = "https://spigotmc.org/" + str(
                                resource[0]["file"]["url"]
                            )
                            try:
                                if resource[0]["file"]["type"] in "external":
                                    embedVar = discord.Embed(
                                        title=resource[0]["name"],
                                        color=discord.Color.from_rgb(
                                            173, 156, 255),
                                    )
                                    embedVar.description = resource[0]["tag"]
                                    embedVar.add_field(
                                        name="Author",
                                        value=author_details_v1["name"],
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Downloads",
                                        value=resource[0]["downloads"],
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Rating",
                                        value=resource[0]["rating"]["average"],
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Tested Versions",
                                        value=str(
                                            resource[0]["testedVersions"])
                                        .replace("[", "")
                                        .replace("]", "")
                                        .replace("'", ""),
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Latest Plugin Version",
                                        value=str(plugin_version["name"]),
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Plugin Versions",
                                        value=str([name["name"]
                                                  for name in spigetv3])
                                        .replace("[", "")
                                        .replace("]", "")
                                        .replace("'", ""),
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Download Type",
                                        value=resource[0]["file"]["type"],
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Download URL",
                                        value=f"{resource[0]['file']['externalUrl']}",
                                        inline=False,
                                    )
                                    embedVar.set_thumbnail(url=str(thumbnail))
                                    await ctx.send(embed=embedVar)
                                else:
                                    embedVar = discord.Embed(
                                        title=resource[0]["name"],
                                        color=discord.Color.from_rgb(
                                            173, 156, 255),
                                    )
                                    embedVar.description = resource[0]["tag"]
                                    embedVar.add_field(
                                        name="Author",
                                        value=author_details_v1["name"],
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Downloads",
                                        value=resource[0]["downloads"],
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Rating",
                                        value=resource[0]["rating"]["average"],
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Tested Versions",
                                        value=str(
                                            resource[0]["testedVersions"])
                                        .replace("[", "")
                                        .replace("]", "")
                                        .replace("'", ""),
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Latest Plugin Version",
                                        value=str(plugin_version["name"]),
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Plugin Versions",
                                        value=str([name["name"]
                                                  for name in spigetv3])
                                        .replace("[", "")
                                        .replace("]", "")
                                        .replace("'", ""),
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Download Info",
                                        value=resource[0]["file"]["type"],
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Download Size",
                                        value=file_size,
                                        inline=True,
                                    )
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
