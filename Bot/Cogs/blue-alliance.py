import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("Blue_Alliance_API_Key")
parser = simdjson.Parser()


class BlueAllianceV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    blueAlliance = SlashCommandGroup("blue-alliance", "Blue Alliance API commands")
    blueAllianceMatches = blueAlliance.create_subgroup(
        "matches", "Blue Alliance match commands"
    )
    blueAllianceTeams = blueAlliance.create_subgroup(
        "teams", "Blue Alliance team commands"
    )

    @blueAllianceTeams.command(name="info")
    async def blueAllianceTeamInfo(
        self, ctx, *, team_number: Option(int, "The FRC team number")
    ):
        """Returns info about an FRC team"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{team_number}",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()

                mainFilter = ["nickname", "team_number"]
                try:
                    if "Error" in dataMain:
                        raise ValueError
                    else:
                        for key, value in dataMain.items():
                            if key not in mainFilter:
                                embed.add_field(name=key, value=value, inline=True)
                                embed.remove_field(-24)
                        embed.title = (
                            f"{dataMain['team_number']} - {dataMain['nickname']}"
                        )
                        await ctx.respond(embed=embed)
                except ValueError:
                    embedError = discord.Embed()
                    embedError.description = "It seems like there are no teams named like that. Please try again"
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @blueAllianceTeams.command(name="events")
    async def blueAllianceTeamEvents(
        self, ctx, *, team_number: Option(int, "The FRC team number")
    ):
        """Returns what events an FRC team has attended"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{team_number}/events",
                headers=headers,
            ) as r:
                data2 = await r.content.read()
                dataMain2 = parser.parse(data2, recursive=True)
                embed = discord.Embed()

                filterMain = ["gmaps_place_id", "name", "webcasts"]
                try:
                    if "Error" in dataMain2:
                        raise ValueError
                    else:
                        for dictItem2 in dataMain2:
                            for key, value in dictItem2.items():
                                if key not in filterMain:
                                    embed.add_field(
                                        name=key, value=f"[{value}]", inline=True
                                    )
                                    embed.remove_field(-24)
                            embed.title = dictItem2["name"]
                            await ctx.respond(embed=embed)
                except ValueError:
                    embedError = discord.Embed()
                    embedError.description = "It seems like there are no teams named like that. Please try again"
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @blueAllianceMatches.command(name="team")
    async def blueAllianceTeamMatches(
        self,
        ctx,
        *,
        team_number: Option(int, "The FRC team number"),
        event_key: Option(str, "The event key"),
    ):
        """Returns the general info for each match that a team was in during the given event"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{team_number}/event/{event_key}/matches",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()

                filter5 = ["score_breakdown", "alliances", "videos", "match_number"]
                try:
                    if "Error" in dataMain:
                        raise ValueError
                    else:
                        for dictItem in dataMain:
                            for key, value in dictItem.items():
                                if key not in filter5:
                                    embed.add_field(name=key, value=value, inline=True)
                            for k, v in dictItem["alliances"]["blue"].items():
                                embed.add_field(name=k, value=v, inline=True)
                            for item, res in dictItem["alliances"]["red"].items():
                                embed.add_field(name=item, value=res, inline=True)
                            embed.title = f"Match {dictItem['match_number']}"
                            await ctx.respond(embed=embed)
                except ValueError:
                    embedError = discord.Embed()
                    embedError.description = "It seems like there are no teams and/or event keys named like that. Please try again"
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @blueAllianceMatches.command(name="breakdown")
    async def blueAllianceBreakdownV2(
        self,
        ctx,
        *,
        frc_team: Option(int, "The FRC team number"),
        event_key: Option(str, "The event key"),
    ):
        """Returns the breakdown of a team's match"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{frc_team}/event/{event_key}/matches",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()
                try:
                    if "Error" in dataMain:
                        raise ValueError
                    else:
                        for dictItem in dataMain:
                            for keys, value in dictItem["score_breakdown"][
                                "blue"
                            ].items():
                                embed.add_field(name=keys, value=value, inline=True)
                            for k, v in dictItem["score_breakdown"]["red"].items():
                                embed.add_field(name=k, value=v, inline=True)
                            embed.title = f"Match {dictItem['match_number']}"
                            await ctx.respond(embed=embed)
                except ValueError:
                    embedError = discord.Embed()
                    embedError.description = "It seems like there are no teams and/or event keys named like that. Please try again"
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @blueAlliance.command(name="rankings")
    async def blueAllianceEventRankings(
        self, ctx, *, frc_event_key: Option(str, "The event key")
    ):
        """Returns the event ranking"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/event/{frc_event_key}/rankings",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    mainPages = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=f'Rank {dictItem["rank"]} - {str(dictItem["team_key"]).replace("frc", "")}'
                            )
                            .add_field(
                                name="Matches Played",
                                value=dictItem["matches_played"],
                                inline=True,
                            )
                            .add_field(
                                name="Records",
                                value=[
                                    f"{k}: {v}".replace("'", "")
                                    for k, v in dictItem["record"].items()
                                ],
                                inline=True,
                            )
                            for dictItem in dataMain["rankings"]
                        ],
                        loop_pages=True,
                    )
                    await mainPages.respond(ctx.interaction, ephemeral=False)
                except KeyError:
                    embedError = discord.Embed()
                    embedError.description = (
                        "It seems like there are no records available. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @blueAllianceMatches.command(name="all")
    async def blueAllianceEventMatches(
        self, ctx, *, frc_event_key: Option(str, "The event key")
    ):
        """Returns all of the matches for an FRC event"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/event/{frc_event_key}/matches/simple",
                headers=headers,
            ) as response:
                data = await response.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if "Error" in dataMain:
                        raise ValueError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                [
                                    discord.Embed(
                                        title=f"Match {dictItem['match_number']} - {dictItem['winning_alliance']}"
                                    )
                                    .add_field(
                                        name="Comp Level",
                                        value=dictItem["comp_level"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Score (Red)",
                                        value=dictItem["alliances"]["red"]["score"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Score (Blue)",
                                        value=dictItem["alliances"]["blue"]["score"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Blue Alliance",
                                        value=[
                                            str(blueTeam).replace("frc", "")
                                            for blueTeam in dictItem["alliances"][
                                                "blue"
                                            ]["team_keys"]
                                        ],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Red Alliance",
                                        value=[
                                            str(redTeam).replace("frc", "")
                                            for redTeam in dictItem["alliances"]["red"][
                                                "team_keys"
                                            ]
                                        ],
                                        inline=True,
                                    )
                                ]
                                for dictItem in dataMain
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except ValueError:
                    embedError = discord.Embed()
                    embedError.description = (
                        "It seems like there are no records available. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(BlueAllianceV1(bot))
