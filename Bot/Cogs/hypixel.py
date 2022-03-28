import asyncio
import os

import aiohttp
import discord
import orjson
import uvloop
from discord.commands import slash_command
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

hypixel_api_key = os.getenv("Hypixel_API_Key")


class hypixel_api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="hypixel-user",
        description="Returns Info About A Minecraft User on Hypixel",
    )
    async def hypixel_user(self, ctx, *, uuid: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"uuid": uuid, "key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/player", params=params
            ) as r:
                player = await r.content.read()
                playerMain = orjson.loads(player)
                try:
                    if str(playerMain["success"]) == "True":
                        discord_embed = discord.Embed(
                            title="Player Info",
                            color=discord.Color.from_rgb(186, 244, 255),
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
                        ]
                        for key, value in playerMain["player"].items():
                            if key not in filterMainV3:
                                discord_embed.add_field(
                                    name=key, value=value, inline=True
                                )
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
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class hypixel_player_count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="hypixel-count",
        description="Returns the Amount of Players in each game server",
    )
    async def player_count(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/counts", params=params
            ) as response:
                status = await response.content.read()
                statusMain = orjson.loads(status)
                try:
                    embedVar = discord.Embed(
                        title="Games Player Count",
                        color=discord.Color.from_rgb(186, 193, 255),
                    )
                    for k, v in statusMain["games"].items():
                        embedVar.add_field(
                            name=k, value=v["players"], inline=True)
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The command broke. Please try again."
                    embedVar.add_field(
                        name="Reason", value=str(e), inline=False)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class hypixel_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="hypixel-player-status",
        description="Returns the given player's online status",
    )
    async def player_status(self, ctx, *, uuid: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"uuid": uuid, "key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/status", params=params
            ) as rep:
                player_statusv3 = await rep.content.read()
                playerStatusMain = orjson.loads(player_statusv3)
                try:
                    if str(playerStatusMain["success"]) == "True":
                        filterKeys = ["session"]
                        embedVar = discord.Embed(
                            title="Player Status",
                            color=discord.Color.from_rgb(222, 222, 222),
                        )
                        for keys, value in playerStatusMain.items():
                            if keys not in filterKeys:
                                embedVar.add_field(
                                    name=keys, value=value, inline=True)
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


class networkPunishments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="hypixel-punishment-stats",
        description="Shows the stats for the amount of punishments given on Hypixel (All Users)",
    )
    async def punishment_stats(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/punishmentstats", params=params
            ) as r:
                stats = await r.content.read()
                statsMain = orjson.loads(stats)
                try:
                    embedVar = discord.Embed(
                        title="Total Amounts of Punishments Given",
                        color=discord.Color.from_rgb(186, 193, 255),
                    )
                    if str(statsMain["success"]) == "True":
                        filterMain4 = ["success"]
                        for keys, value in statsMain.items():
                            if keys not in filterMain4:
                                embedVar.add_field(
                                    name=keys, value=value, inline=True)
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
                    embedException.add_field(
                        name="Reason", value=e, inline=True)
                    embedException.add_field(
                        name="HTTP Response Status", value=r.status, inline=True
                    )
                    await ctx.respond(embed=embedException)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(hypixel_api(bot))
    bot.add_cog(hypixel_status(bot))
    bot.add_cog(hypixel_player_count(bot))
    bot.add_cog(networkPunishments(bot))
