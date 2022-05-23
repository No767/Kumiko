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
from exceptions import NoItemsError

load_dotenv()

api_key = os.getenv("FIRST_Events_Final_Key")
parser = simdjson.Parser()


class FirstFRCV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    frc = SlashCommandGroup("frc", "Commands for the FIRST FRC API")
    events = frc.create_subgroup("events", "Commands for Events")

    @frc.command(name="season")
    async def frcSeason(
        self, ctx, *, season: Option(int, "The year of the event (eg 2020, 2021, etc)")
    ):
        """Returns the season summary for the current FRC season (may cause spam)"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}", headers=headers
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    filterSeason = ["frcChampionships", "gameName"]
                    embedVar = discord.Embed()
                    for k, v in dataMain.items():
                        if k not in filterSeason:
                            embedVar.add_field(name=k, value=v, inline=True)
                    for dictItem in dataMain["frcChampionships"]:
                        for keys, value in dictItem.items():
                            embedVar.add_field(
                                name=f"frc_championship_{keys}",
                                value=value,
                                inline=True,
                            )
                    embedVar.title = dataMain["gameName"]
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = (
                        "You may have incorrectly put in data here. Please try again"
                    )
                    embedError.add_field(name="Error", value=e, inline=True)
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
                try:
                    data = await re.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    filterMain2 = ["matchLevel", "matchNumber"]
                    embedVar = discord.Embed()
                    try:
                        if len(dataMain["MatchScores"]) == 0:
                            raise NoItemsError
                        else:
                            for dictItem in dataMain["MatchScores"]:
                                embedVar.title = f"{dictItem['matchLevel']} #{dictItem['matchNumber']}"
                                for dictItem2 in dictItem["alliances"]:
                                    for keys, value in dictItem2.items():
                                        if keys not in filterMain2:
                                            embedVar.add_field(
                                                name=keys, value=value, inline=True
                                            )
                                            embedVar.remove_field(-42)
                                    await ctx.respond(embed=embedVar)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = (
                            "It seems like there are no scores... Please try again"
                        )
                        await ctx.respond(embed=embedNoItemsError)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Something went wrong. Please try again..."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedError)

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
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    try:
                        filterResults = ["teams", "description"]
                        embedVar = discord.Embed()
                        for dictItemMain in dataMain["Matches"]:
                            for key, value in dictItemMain.items():
                                if key not in filterResults:
                                    embedVar.add_field(
                                        name=key, value=value, inline=True
                                    )
                                    embedVar.remove_field(-15)
                            embedVar.add_field(
                                name="Teams",
                                value=str(
                                    [
                                        f'{item["teamNumber"]} - {item["station"]}'
                                        for item in dictItemMain["teams"]
                                    ]
                                ).replace("'", ""),
                                inline=True,
                            )
                            embedVar.remove_field(0)
                            embedVar.title = dictItemMain["description"]
                            await ctx.respond(embed=embedVar)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = (
                            "It seems like there are no results... Please try again"
                        )
                        await ctx.respond(embed=embedNoItemsError)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Something went wrong. Please try again..."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedError)

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
                try:
                    data = await res.content.read()
                    dataMain2 = parser.parse(data, recursive=True)
                    try:
                        if len(dataMain2["Events"]) == 0:
                            raise NoItemsError
                        else:
                            filterEvents = ["name"]
                            embed = discord.Embed()
                            for dictItem in dataMain2["Events"]:
                                for keys, value in dictItem.items():
                                    if keys not in filterEvents:
                                        embed.add_field(
                                            name=keys, value=value, inline=True
                                        )
                                        embed.remove_field(-18)
                                embed.title = dictItem["name"]
                                await ctx.respond(embed=embed)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = "Sorry, it seems like there is no events during those times! Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = (
                        "You may have incorrectly put in data here. Please try again"
                    )
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @events.command(name="top")
    async def frcEventRanking(
        self,
        ctx,
        *,
        season: Option(str, "The FRC season year"),
        event_code: Option(str, "The FRC event code "),
    ):
        """Returns the top 10 FRC teams within a given event"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            params = {"top": 10}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}/rankings/{event_code}",
                headers=headers,
                params=params,
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    try:
                        if len(dataMain["Rankings"]) == 0:
                            raise NoItemsError
                        else:
                            filterResults = ["rank", "teamNumber"]
                            embedVar = discord.Embed()
                            for dictItemMain in dataMain["Rankings"]:
                                for k, v in dictItemMain.items():
                                    if k not in filterResults:
                                        embedVar.add_field(name=k, value=v, inline=True)
                                        embedVar.remove_field(-11)
                                embedVar.title = f"Rank {dictItemMain['rank']} - {dictItemMain['teamNumber']}"
                                await ctx.respond(embed=embedVar)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = (
                            "It seems like there are no teams... Please try again"
                        )
                        await ctx.respond(embed=embedNoItemsError)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Something went wrong. Please try again..."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedError)

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
                try:
                    data = await r.content.read()
                    try:
                        dataMain = parser.parse(data, recursive=True)
                        filterEventSchedule = ["teams", "description"]
                        embedVar = discord.Embed()

                        for dictItem in dataMain["Schedule"]:
                            for key, value in dictItem.items():
                                if key not in filterEventSchedule:
                                    embedVar.add_field(
                                        name=key, value=value, inline=True
                                    )
                                    embedVar.remove_field(-4)
                            embedVar.title = dictItem["description"]
                            embedVar.description = str(
                                [
                                    f'{item["teamNumber"]} - {item["station"]}'
                                    for item in dictItem["teams"]
                                ]
                            ).replace("'", "")
                            await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedValueError = discord.Embed()
                        embedValueError.description = "There seems to be no seasons, event codes, or teams... Please try again"
                        await ctx.respond(embed=embedValueError)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Something went wrong. Please try again..."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedError)

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
                    dataMain = parser.parse(data, recursive=True)
                    filterEventAlliances = [
                        "number",
                        "name",
                        "captain",
                        "round1",
                        "round2",
                    ]
                    embedVar = discord.Embed()
                    for dictItem in dataMain["Alliances"]:
                        for key, value in dictItem.items():
                            if key not in filterEventAlliances:
                                embedVar.add_field(name=key, value=value, inline=True)
                                embedVar.remove_field(-4)
                        embedVar.title = dictItem["name"]
                        embedVar.description = f"{dictItem['captain']} - {dictItem['round1']} - {dictItem['round2']}"
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Something went wrong. Please try again..."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @frc.command(name="awards")
    async def frcTeamAwards(
        self,
        ctx,
        *,
        season: Option(str, "The FRC season year"),
        team_number: Option(str, "The FRC team number (eg 5507)"),
    ):
        """Returns a list of events that the given team has gotten"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": f"Basic {api_key}", "If-Modified-Since": ""}
            async with session.get(
                f"https://frc-api.firstinspires.org/v3.0/{season}/awards/team/{team_number}",
                headers=headers,
            ) as response:
                try:
                    data = await response.content.read()
                    dataMain3 = parser.parse(data, recursive=True)
                    try:
                        if len(dataMain3["Awards"]) == 0:
                            raise NoItemsError
                        else:
                            filterAwards = ["fullTeamName", "name"]
                            embedMain = discord.Embed()
                            for dictItem in dataMain3["Awards"]:
                                for awardKeys, awardValues in dictItem.items():
                                    if awardKeys not in filterAwards:
                                        embedMain.add_field(
                                            name=awardKeys,
                                            value=awardValues,
                                            inline=True,
                                        )
                                        embedMain.remove_field(-10)
                                embedMain.title = dictItem["name"]
                                await ctx.respond(embed=embedMain)
                    except NoItemsError:
                        embedErrorMain = discord.Embed()
                        embedErrorMain.description = (
                            "It seems like there are no awards... Please try again"
                        )
                        await ctx.respond(embed=embedErrorMain)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Something went wrong. Please try again..."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(FirstFRCV1(bot))
