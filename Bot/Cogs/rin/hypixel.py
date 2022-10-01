import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from rin_exceptions import NotFoundHTTPException

load_dotenv()

hypixel_api_key = os.getenv("Hypixel_API_Key")
parser = simdjson.Parser()


class HypixelV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    hypixel = SlashCommandGroup("hypixel", "Commands for Hypixel")

    @hypixel.command(name="count")
    async def player_count(self, ctx):
        """Returns the amount of players in each game server"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/counts", params=params
            ) as response:
                status = await response.content.read()
                statusMain = parser.parse(status, recursive=True)
                try:
                    if statusMain["success"] is False or response.status == 400:
                        raise NotFoundHTTPException
                    else:
                        embedVar = discord.Embed(
                            title="Games Player Count",
                            color=discord.Color.from_rgb(186, 193, 255),
                        )
                        for k, v in statusMain["games"].items():
                            embedVar.add_field(name=k, value=v["players"], inline=True)
                        await ctx.respond(embed=embedVar)
                except NotFoundHTTPException:
                    await ctx.respond(
                        embed=discord.Embed(
                            description="Oops, it seems like there was an error. Please try again"
                        )
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @hypixel.command(name="punishments")
    async def punishment_stats(self, ctx):
        """Shows the stats for the amount of punishments given on Hypixel (All Users)"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/punishmentstats", params=params
            ) as r:
                stats = await r.content.read()
                statsMain = parser.parse(stats, recursive=True)
                embedVar = discord.Embed(
                    title="Total Amounts of Punishments Given",
                    color=discord.Color.from_rgb(186, 193, 255),
                )
                try:
                    if statsMain["success"] is False or r.status == 400:
                        raise NotFoundHTTPException
                    else:
                        for k, v in statsMain.items():
                            if k not in ["success"]:
                                embedVar.add_field(name=k, value=v, inline=True)
                        await ctx.respond(embed=embedVar)
                except NotFoundHTTPException:
                    embedError = discord.Embed()
                    embedError.description = (
                        "There seems to be an error... Please try again"
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(HypixelV1(bot))
