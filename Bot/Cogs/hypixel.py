import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from exceptions import UnknownPlayer

load_dotenv()

hypixel_api_key = os.getenv("Hypixel_API_Key")
parser = simdjson.Parser()


class HypixelV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    hypixel = SlashCommandGroup("hypixel", "Commands for Hypixel")
    hypixelPlayer = hypixel.create_subgroup("player", "Commands for Hypixel Player")

    @hypixelPlayer.command(name="info")
    async def hypixel_user(
        self, ctx, *, uuid: Option(str, "The UUID of the minecraft player")
    ):
        """Returns info about an minecraft user on Hypixel"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"uuid": uuid, "key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/player", params=params
            ) as r:
                player = await r.content.read()
                playerMain = parser.parse(player, recursive=True)
                try:
                    if str(playerMain["success"]) == "True":
                        discord_embed = discord.Embed(
                            color=discord.Color.from_rgb(186, 244, 255)
                        )
                        filterMainV3 = [
                            "achievements",
                            "achievementsOneTime",
                            "stats",
                            "petConsumables",
                            "monthlycrates",
                            "parkourCheckpointBests",
                            "parkourCompletions",
                            "quests",
                            "housingMeta",
                            "firstLogin",
                            "lastLogin",
                            "knownAliasesLower",
                            "vanityMeta",
                            "lastAdsenseGenerateTime",
                            "lastLogout",
                            "challenges",
                            "adventRewards2020",
                            "achievementRewardsNew",
                            "adsense_tokens",
                            "displayname",
                        ]
                        if "None" in playerMain["player"]:
                            raise UnknownPlayer
                        else:
                            for key, value in playerMain["player"].items():
                                if key not in filterMainV3:
                                    discord_embed.add_field(
                                        name=key, value=value, inline=True
                                    )
                            discord_embed.title = playerMain["player"]["displayname"]
                            await ctx.respond(embed=discord_embed)
                    else:
                        embedVar = discord.Embed()
                        embedVar.description = "The query was not successful"
                        embedVar.add_field(
                            name="Success", value=playerMain["success"], inline=True
                        )
                        embedVar.add_field(
                            name="Cause", value=playerMain["cause"], inline=True
                        )
                        embedVar.add_field(
                            name="HTTP Response Status", value=r.status, inline=True
                        )
                        await ctx.respond(embed=embedVar)
                except UnknownPlayer:
                    embedValError = discord.Embed()
                    embedValError.description = "It seems like that the player wasn't online.... Please try again"
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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

    @hypixelPlayer.command(name="status")
    async def player_status(
        self, ctx, *, uuid: Option(str, "The UUID of the minecraft player")
    ):
        """Shows the current status of the player given"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"uuid": uuid, "key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/status", params=params
            ) as rep:
                player_statusv3 = await rep.content.read()
                playerStatusMain = parser.parse(player_statusv3, recursive=True)
                try:
                    if str(playerStatusMain["success"]) == "True":
                        filterKeys = ["session"]
                        embedVar = discord.Embed(
                            title="Player Status",
                            color=discord.Color.from_rgb(222, 222, 222),
                        )
                        for keys, value in playerStatusMain.items():
                            if keys not in filterKeys:
                                embedVar.add_field(name=keys, value=value, inline=True)
                        for k, v in playerStatusMain["session"].items():
                            embedVar.add_field(name=k, value=v, inline=True)
                        await ctx.respond(embed=embedVar)
                    else:
                        embedVar = discord.Embed()
                        embedVar.description = "The query was not successful"
                        embedVar.add_field(
                            name="Success",
                            value=playerStatusMain["success"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Cause", value=playerStatusMain["cause"], inline=True
                        )
                        embedVar.add_field(
                            name="HTTP Reponse Status", value=rep.status, inline=True
                        )
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
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
