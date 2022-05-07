import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("Blue_Alliance_API_Key")
parser = simdjson.Parser()


class BlueAllianceV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="blue-alliance-team-info",
        description="Provides info about an FRC team",
        guild_ids=[866199405090308116],
    )
    async def blueAllianceTeamInfo(
        self, ctx, *, team_number: Option(int, "The FRC team number")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{team_number}",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()
                embedError = discord.Embed()
                mainFilter = ["nickname", "team_number"]
                try:
                    for key, value in dataMain.items():
                        if key not in mainFilter:
                            embed.add_field(name=key, value=value, inline=True)
                            embed.remove_field(-24)
                    embed.title = f"{dataMain['team_number']} - {dataMain['nickname']}"
                    await ctx.respond(embed=embed)
                except Exception as e:
                    embedError.description = (
                        "Oops, something went wrong. Please try again..."
                    )
                    embedError.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class BlueAllianceV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="blue-alliance-team-events",
        description="Return what events an FRC team has attended",
        guild_ids=[866199405090308116],
    )
    async def blueAllianceTeamEvents(
        self, ctx, *, team_number: Option(int, "The FRC team number")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{team_number}/events",
                headers=headers,
            ) as r:
                data2 = await r.content.read()
                dataMain2 = parser.parse(data2, recursive=True)
                embed = discord.Embed()
                embedError = discord.Embed()
                filterMain = ["gmaps_place_id", "name", "webcasts"]
                try:
                    for dictItem2 in dataMain2:
                        for key, value in dictItem2.items():
                            if key not in filterMain:
                                embed.add_field(
                                    name=key, value=f"[{value}]", inline=True
                                )
                                embed.remove_field(-24)
                        embed.title = dictItem2["name"]
                        await ctx.respond(embed=embed)
                except Exception as e:
                    embedError.description = (
                        "Oops, something went wrong. Please try again..."
                    )
                    embedError.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedError)


class BlueAllianceV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="blue-alliance-team-matches-info",
        description="Returns the general info for each match that a team was in during the given event",
        guild_ids=[866199405090308116],
    )
    async def blueAllianceTeamMatches(
        self,
        ctx,
        *,
        team_number: Option(int, "The FRC team number"),
        event_key: Option(str, "The event key"),
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{team_number}/event/{event_key}/matches",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()
                embedError = discord.Embed()
                filter = ["score_breakdown", "alliances", "videos", "match_number"]
                try:
                    for dictItem in dataMain:
                        for key, value in dictItem.items():
                            if key not in filter:
                                embed.add_field(name=key, value=value, inline=True)
                        for k, v in dictItem["alliances"]["blue"].items():
                            embed.add_field(name=k, value=v, inline=True)
                        for item, res in dictItem["alliances"]["red"].items():
                            embed.add_field(name=item, value=res, inline=True)
                        embed.title = f"Match {dictItem['match_number']}"
                        await ctx.respond(embed=embed)
                except Exception as e:
                    embedError.description = (
                        "Oops, something went wrong. Please try again..."
                    )
                    embedError.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedError)


class BlueAllianceV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="blue-alliance-team-match-breakdown",
        description="Returns the breakdown of a team's match",
        guild_ids=[866199405090308116],
    )
    async def blueAllianceBreakdown(
        self,
        ctx,
        *,
        frc_team_number: Option(int, "The FRC team number"),
        frc_event_key: Option(str, "The event key"),
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{frc_team_number}/event/{frc_event_key}/matches",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()
                for dictItem in dataMain:
                    for keys, value in dictItem["score_breakdown"]["blue"].items():
                        embed.add_field(name=keys, value=value, inline=True)
                    for k, v in dictItem["score_breakdown"]["red"].items():
                        embed.add_field(name=k, value=v, inline=True)
                    embed.title = f"Match {dictItem['match_number']}"
                    await ctx.respond(embed=embed)


class BlueAllianceV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="blue-alliance-event-rankings",
        description="Returns the event ranking",
        guild_ids=[866199405090308116],
    )
    async def blueAllianceEventRankings(
        self, ctx, *, frc_event_key: Option(str, "The event key")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/event/{frc_event_key}/rankings",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()
                filter = ["rank", "record"]
                for dictItem in dataMain["rankings"]:
                    for keys, values in dictItem.items():
                        if keys not in filter:
                            embed.add_field(name=keys, value=values, inline=True)
                    for k, v in dictItem["record"].items():
                        embed.add_field(name=k, value=v, inline=True)
                    embed.title = f"Rank {dictItem['rank']}"
                    await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(BlueAllianceV1(bot))
    bot.add_cog(BlueAllianceV2(bot))
    bot.add_cog(BlueAllianceV3(bot))
    # bot.add_cog(BlueAllianceV4(bot)) # having some issues rn for some reason. will fix later
    bot.add_cog(BlueAllianceV5(bot))
