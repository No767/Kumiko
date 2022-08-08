import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from rin_exceptions import NotFoundHTTPException

parser = simdjson.Parser()


class MCSrvStatsV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mc = SlashCommandGroup("minecraft", "Commands for Minecraft Server Stats")

    @mc.command(name="java")
    async def javaCheck(
        self, ctx, *, server: Option(str, "The Minecraft server IP or hostname")
    ):
        """Checks and returns info about the given Minecraft Java server"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.mcsrvstat.us/2/{server}") as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                filterJava = ["motd", "debug", "icon", "players", "hostname"]
                embed = discord.Embed()
                try:
                    if dataMain["online"] is False or r.status == 404:
                        raise NotFoundHTTPException
                    else:
                        for key, val in dataMain.items():
                            if key not in filterJava:
                                embed.add_field(name=key, value=val, inline=True)
                        for k, v in dataMain["players"].items():
                            embed.add_field(name=k, value=v, inline=True)
                        embed.title = dataMain["hostname"]
                        embed.description = str(dataMain["motd"]["clean"])
                        embed.set_thumbnail(
                            url=f"https://api.mcsrvstat.us/icon/{server}"
                        )
                        await ctx.respond(embed=embed)
                except NotFoundHTTPException:
                    await ctx.respond(
                        embed=discord.Embed(
                            description="It seems like the server requested is offline. Please try again."
                        )
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mc.command(name="bedrock")
    async def bedrockCheck(
        self, ctx, *, server: Option(str, "The Minecraft server IP or hostname")
    ):
        """Returns the status and info of any Bedrock or Geyser-compatible server"""
        async with aiohttp.ClientSession(json_serialize=orjson.loads) as session:
            async with session.get(f"https://api.mcsrvstat.us/bedrock/2/{server}") as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()
                filterBedrock = ["motd", "debug", "players", "hostname"]
                try:
                    if dataMain["online"] is False or r.status == 404:
                        raise NotFoundHTTPException
                    else:
                        for key, val in dataMain.items():
                            if key not in filterBedrock:
                                embed.add_field(name=key, value=val, inline=True)
                        for k, v in dataMain["players"].items():
                            embed.add_field(name=k, value=v, inline=True)
                        embed.title = dataMain["hostname"]
                        embed.description = str(dataMain["motd"]["clean"])
                        embed.set_thumbnail(
                            url=f"https://api.mcsrvstat.us/icon/{server}"
                        )
                        await ctx.respond(embed=embed)
                except NotFoundHTTPException:
                    await ctx.respond(
                        embed=discord.Embed(
                            description="It seems like the server requested is offline. Please try again."
                        )
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(MCSrvStatsV1(bot))
