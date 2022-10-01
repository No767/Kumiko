import asyncio
import os
from datetime import datetime

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from rin_exceptions import NoItemsError

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
                        raise NoItemsError
                    else:
                        for key, value in dataMain.items():
                            if key not in mainFilter:
                                embed.add_field(name=key, value=value, inline=True)
                                embed.remove_field(-24)
                        embed.title = (
                            f"{dataMain['team_number']} - {dataMain['nickname']}"
                        )
                        await ctx.respond(embed=embed)
                except NoItemsError:
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
                try:
                    if "Error" in dataMain2:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(title=mainItem["name"])
                                .add_field(
                                    name="Event Location Address",
                                    value=mainItem["address"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Event Location Name",
                                    value=mainItem["location_name"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Event Key", value=mainItem["key"], inline=True
                                )
                                .add_field(
                                    name="Event Type",
                                    value=mainItem["event_type_string"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Start Date",
                                    value=mainItem["start_date"],
                                    inline=True,
                                )
                                .add_field(
                                    name="End Date",
                                    value=mainItem["end_date"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Timezone",
                                    value=mainItem["timezone"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Week", value=mainItem["week"], inline=True
                                )
                                .add_field(
                                    name="Year", value=mainItem["year"], inline=True
                                )
                                for mainItem in dataMain2
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
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
                try:
                    if "Error" in dataMain:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(title=f'Match {mainItem["match_number"]}')
                                .add_field(
                                    name="Blue Alliance Teams",
                                    value=mainItem["alliances"]["blue"]["team_keys"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Blue Alliance Total Points",
                                    value=mainItem["score_breakdown"]["blue"][
                                        "totalPoints"
                                    ],
                                    inline=True,
                                )
                                .add_field(
                                    name="Blue Alliance Total Score",
                                    value=mainItem["alliances"]["blue"]["score"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Red Alliance Teams",
                                    value=mainItem["alliances"]["red"]["team_keys"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Red Alliance Total Points",
                                    value=mainItem["score_breakdown"]["red"][
                                        "totalPoints"
                                    ],
                                    inline=True,
                                )
                                .add_field(
                                    name="Red Alliance Total Score",
                                    value=mainItem["alliances"]["red"]["score"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Predicted Time",
                                    value=datetime.fromtimestamp(
                                        mainItem["predicted_time"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Actual Time",
                                    value=datetime.fromtimestamp(
                                        mainItem["actual_time"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Winning Alliance",
                                    value=mainItem["winning_alliance"],
                                    inline=True,
                                )
                                for mainItem in dataMain
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
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
                        raise NoItemsError
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
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = (
                        "It seems like there are no records available. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(BlueAllianceV1(bot))
