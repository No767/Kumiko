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
                    embedVar = discord.Embed(
                        title="Games Player Count",
                        color=discord.Color.from_rgb(186, 193, 255),
                    )
                    for k, v in statusMain["games"].items():
                        embedVar.add_field(name=k, value=v["players"], inline=True)
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The command broke. Please try again."
                    embedVar.add_field(name="Reason", value=str(e), inline=False)
                    await ctx.respond(embed=embedVar)

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
                try:
                    embedVar = discord.Embed(
                        title="Total Amounts of Punishments Given",
                        color=discord.Color.from_rgb(186, 193, 255),
                    )
                    if str(statsMain["success"]) == "True":
                        filterMain4 = ["success"]
                        for keys, value in statsMain.items():
                            if keys not in filterMain4:
                                embedVar.add_field(name=keys, value=value, inline=True)
                        await ctx.respond(embed=embedVar)
                    else:
                        embedVar.description = "The results didn't come through..."
                        embedVar.add_field(
                            name="Success", value=statsMain["success"], inline=True
                        )
                        embedVar.add_field(
                            name="Cause", value=statsMain["cause"], inline=True
                        )
                        embedVar.add_field(
                            name="HTTP Response Status", value=r.status, inline=True
                        )
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedException = discord.Embed()
                    embedException.description = "The query failed..."
                    embedException.add_field(name="Reason", value=e, inline=True)
                    embedException.add_field(
                        name="HTTP Response Status", value=r.status, inline=True
                    )
                    await ctx.respond(embed=embedException)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(HypixelV1(bot))
