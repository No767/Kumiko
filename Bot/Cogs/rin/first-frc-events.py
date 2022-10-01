import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from rin_exceptions import NoItemsError, NotFoundHTTPException

load_dotenv()

api_key = os.getenv("FIRST_Events_Final_Key")
jsonParser = simdjson.Parser()


class FirstFRCV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    frc = SlashCommandGroup("frc", "Commands for the FIRST FRC API")
    events = frc.create_subgroup("events", "Commands for Events")

    @frc.command(name="season")
    async def frcSeason(
        self, ctx, *, season: Option(int, "The year of the event (eg 2020, 2021, etc)")
    ):
        """Returns the season summary for the current FRC season"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}", headers=headers
            ) as r:
                try:
                    if r.status == 400:
                        raise NotFoundHTTPException
                    else:
                        data = await r.content.read()
                        dataMain = jsonParser.parse(data, recursive=True)
                        filterSeason = ["frcChampionships", "gameName", "kickoff"]
                        embedVar = discord.Embed()
                        for k, v in dataMain.items():
                            if k not in filterSeason:
                                embedVar.add_field(name=k, value=v, inline=True)
                        embedVar.add_field(
                            name="Kickoff",
                            value=parser.isoparse(dataMain["kickoff"]).strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),
                            inline=True,
                        )
                        embedVar.title = dataMain["gameName"]
                        await ctx.respond(embed=embedVar)
                except NotFoundHTTPException:
                    embedError = discord.Embed()
                    embedError.description = "Oops, but there seem to be no data for that season. Please try again."
                    await ctx.respond(embed=embedError)
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @frc.command(name="score")
    async def frcScoreDetails(
        self,
        ctx,
        *,
        season: Option(str, "The FRC season year"),
        event_code: Option(str, "The FRC event code "),
        tournament_level: Option(
            str,
            "The FRC tournament level",
            choices=["qual", "playoff"],
        ),
        match_number: Option(str, "The FRC match number"),
    ):
        """Returns the FRC team's score details for a given event"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            params = {"matchNumber": match_number}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}/scores/{event_code}/{tournament_level}",
                headers=headers,
                params=params,
            ) as re:
                data = await re.content.read()
                try:
                    dataMain = jsonParser.parse(data, recursive=True)
                    try:
                        if len(dataMain["MatchScores"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=f'{dictItem["matchLevel"]} {dictItem["matchNumber"]}'
                                    )
                                    .add_field(
                                        name="Total Points",
                                        value=[
                                            f'{items["alliance"]}: {items["totalPoints"]}'
                                            for items in dictItem["alliances"]
                                        ],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Ranking Points",
                                        value=[
                                            f'{items["alliance"]}: {items["rp"]}'
                                            for items in dictItem["alliances"]
                                        ],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Foul Points",
                                        value=[
                                            f'{items["alliance"]}: {items["foulPoints"]}'
                                            for items in dictItem["alliances"]
                                        ],
                                        inline=True,
                                    )
                                    for dictItem in dataMain["MatchScores"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = (
                            "It seems like there are no scores... Please try again"
                        )
                        await ctx.respond(embed=embedNoItemsError)
                except ValueError:
                    embedValError = discord.Embed()
                    embedValError.description = "It seems like there wasn't any found based on the search results. Please try again."
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @frc.command(name="results")
    async def frcResults(
        self,
        ctx,
        *,
        season: Option(str, "The FRC season year"),
        event_code: Option(str, "The FRC event code "),
        tournament_level: Option(
            str,
            "The FRC tournament level",
            choices=["qual", "playoff"],
        ),
        team_number: Option(str, "The FRC team number"),
    ):
        """Returns the FRC team's results for a given event (the results of each matches that the team is in)"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            params = {"tournamentLevel": tournament_level, "teamNumber": team_number}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}/matches/{event_code}",
                headers=headers,
                params=params,
            ) as r:
                data = await r.content.read()
                try:
                    dataMain = jsonParser.parse(data, recursive=True)
                    try:
                        if len(dataMain) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(title=mainItem["description"])
                                    .add_field(
                                        name="Red Alliance Final",
                                        value=mainItem["scoreRedFinal"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Red Alliance Foul",
                                        value=mainItem["scoreRedFoul"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Red Alliance Auto",
                                        value=mainItem["scoreRedAuto"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Blue Alliance Final",
                                        value=mainItem["scoreBlueFinal"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Blue Alliance Foul",
                                        value=mainItem["scoreBlueFoul"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Blue Alliance Auto",
                                        value=mainItem["scoreBlueAuto"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Start Time",
                                        value=parser.isoparse(
                                            mainItem["actualStartTime"]
                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Post Results Time",
                                        value=parser.isoparse(
                                            mainItem["postResultTime"]
                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Teams",
                                        value=str(
                                            [
                                                f'{items["station"]}:{items["teamNumber"]}'
                                                for items in mainItem["teams"]
                                            ]
                                        ).replace("'", ""),
                                        inline=True,
                                    )
                                    for mainItem in dataMain["Matches"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = (
                            "It seems like there are no results... Please try again"
                        )
                        await ctx.respond(embed=embedNoItemsError)
                except ValueError:
                    embedValError = discord.Embed()
                    embedValError.description = "It seems like there wasn't any found based on the search results. Please try again."
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @events.command(name="list")
    async def frcEvents(
        self,
        ctx,
        *,
        season: Option(int, "The year of the event (eg 2020, 2021, etc)"),
        tournament_type: Option(
            str,
            "The Type of event to include",
            choices=[
                "None",
                "Regional",
                "DistrictEvent",
                "DistrictChampionship",
                "DistrictChampionshipWithLevels",
                "DistrictChampionshipDivision",
                "ChampionshipSubdivision",
                "ChampionshipDivision",
                "Championship",
            ],
        ),
        week_number: Option(
            str,
            "The week during the FRC season that the event will take place",
            required=False,
        ),
        team_number: Option(
            str,
            "The FRC team number that will be competing at the event (eg 5507)",
            required=False,
        ),
    ):
        """Returns events for the current FRC season"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            params = {
                "tournamentType": f"{tournament_type}",
                "weekNumber": f"{week_number}",
                "teamNumber": f"{team_number}",
            }
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}/events",
                headers=headers,
                params=params,
            ) as res:
                data = await res.content.read()
                try:
                    dataMain2 = jsonParser.parse(data, recursive=True)
                    try:
                        if len(dataMain2["Events"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(title=mainItem["name"])
                                    .add_field(
                                        name="Code", value=mainItem["code"], inline=True
                                    )
                                    .add_field(
                                        name="Division Code",
                                        value=mainItem["divisionCode"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Location",
                                        value=f'{mainItem["city"]}, {mainItem["stateprov"]}, {mainItem["country"]}',
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Timezone",
                                        value=mainItem["timezone"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Start Date",
                                        value=parser.isoparse(
                                            mainItem["dateStart"]
                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                        inline=True,
                                    )
                                    .add_field(
                                        name="End Date",
                                        value=parser.isoparse(
                                            mainItem["dateEnd"]
                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Webcasts",
                                        value=mainItem["webcasts"],
                                        inline=True,
                                    )
                                    for mainItem in dataMain2["Events"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = "Sorry, it seems like there is no events during those times! Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except ValueError:
                    embedValError = discord.Embed()
                    embedValError.description = "It seems like there wasn't any found based on the search results. Please try again."
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @events.command(name="top")
    async def frcEventRanking(
        self,
        ctx,
        *,
        season: Option(str, "The FRC season year"),
        event_code: Option(str, "The FRC event code "),
    ):
        """Returns the top 25 FRC teams within a given event"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            params = {"top": 25}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}/rankings/{event_code}",
                headers=headers,
                params=params,
            ) as r:
                data = await r.content.read()
                try:
                    dataMain = jsonParser.parse(data, recursive=True)
                    try:
                        if len(dataMain["Rankings"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=f'Rank {mainItem["rank"]} - {mainItem["teamNumber"]}'
                                    )
                                    .add_field(
                                        name="Wins", value=mainItem["wins"], inline=True
                                    )
                                    .add_field(
                                        name="Losses",
                                        value=mainItem["losses"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Ties", value=mainItem["ties"], inline=True
                                    )
                                    .add_field(
                                        name="Qual Average",
                                        value=mainItem["qualAverage"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Matches Played",
                                        value=mainItem["matchesPlayed"],
                                        inline=True,
                                    )
                                    for mainItem in dataMain["Rankings"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = (
                            "It seems like there are no teams... Please try again"
                        )
                        await ctx.respond(embed=embedNoItemsError)
                except ValueError:
                    embedValError = discord.Embed()
                    embedValError.description = "It seems like there wasn't any found based on the search results. Please try again."
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @events.command(name="schedule")
    async def frcEventSchedule(
        self,
        ctx,
        *,
        season: Option(str, "The FRC season year"),
        event_code: Option(str, "The FRC event code "),
        tournament_level: Option(
            str,
            "The FRC tournament level",
            choices=["qual", "playoff"],
        ),
        team_number: Option(int, "The FRC team number"),
    ):
        """Returns the schedule for a given FRC event"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            params = {"tournamentLevel": tournament_level, "teamNumber": team_number}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}/schedule/{event_code}",
                headers=headers,
                params=params,
            ) as r:
                data = await r.content.read()
                try:
                    dataMain = jsonParser.parse(data, recursive=True)
                    try:
                        if len(dataMain["Schedule"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(title=mainItem["description"])
                                    .add_field(
                                        name="TournamentLevel",
                                        value=mainItem["tournamentLevel"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Start Time",
                                        value=parser.isoparse(
                                            mainItem["startTime"]
                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Teams",
                                        value=str(
                                            [
                                                f'{items["station"]}:{items["teamNumber"]}'
                                                for items in mainItem["teams"]
                                            ]
                                        ).replace("'", ""),
                                        inline=True,
                                    )
                                    for mainItem in dataMain["Schedule"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedValueError = discord.Embed()
                        embedValueError.description = "There seems to be no seasons, event codes, or teams... Please try again"
                        await ctx.respond(embed=embedValueError)
                except ValueError:
                    embedValError = discord.Embed()
                    embedValError.description = "It seems like there wasn't any found based on the search results. Please try again."
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @events.command(name="alliances")
    async def frcEventAlliances(
        self,
        ctx,
        *,
        season: Option(str, "The FRC season year"),
        event_code: Option(str, "The FRC event code "),
    ):
        """Returns the alliances within an given event"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}/alliances/{event_code}",
                headers=headers,
            ) as r:
                try:
                    data = await r.content.read()
                    try:
                        dataMain = jsonParser.parse(data, recursive=True)
                        if len(dataMain["Alliances"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(title=mainItem["name"])
                                    .add_field(
                                        name="Captain Team",
                                        value=mainItem["captain"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="First Pick",
                                        value=mainItem["round1"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Second Pick",
                                        value=mainItem["round2"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Third Pick",
                                        value=mainItem["round3"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Backup Team",
                                        value=mainItem["backup"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Backup Replaced",
                                        value=mainItem["backupReplaced"],
                                        inline=True,
                                    )
                                    for mainItem in dataMain["Alliances"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except ValueError:
                        embedValError = discord.Embed()
                        embedValError.description = "It seems like there wasn't any found based on the search results. Please try again."
                        await ctx.respond(embed=embedValError)
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = "It seems like there were no alliances... Probably due to bad data input. Please try again"
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(FirstFRCV1(bot))
