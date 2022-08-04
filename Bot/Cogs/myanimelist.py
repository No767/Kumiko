import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from rin_exceptions import HTTPException, NoItemsError

parser = simdjson.Parser()


class MALV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mal = SlashCommandGroup("mal", "Commands for the MyAnimeList/Jikan service")
    malSeasons = mal.create_subgroup("seasons", "Sub commands for anime seasons")
    malRandom = mal.create_subgroup("random", "Random Anime/Manga Commands")

    @mal.command(name="anime")
    async def anime(self, ctx, *, anime_name: Option(str, "Name of the anime")):
        """Fetches up to 25 anime from MAL"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"limit": 25, "q": anime_name, "sfw": "true", "order_by": "title"}
            async with session.get(
                "https://api.jikan.moe/v4/anime/", params=params
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if len(dataMain["data"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=f'{mainItem["title"]}',
                                    description=mainItem["synopsis"],
                                )
                                .add_field(
                                    name="Japanese Title",
                                    value=mainItem["title_japanese"],
                                )
                                .add_field(
                                    name="Score", value=mainItem["score"], inline=True
                                )
                                .add_field(
                                    name="Rating", value=mainItem["rating"], inline=True
                                )
                                .add_field(
                                    name="MAL Rank", value=mainItem["rank"], inline=True
                                )
                                .add_field(
                                    name="Aired",
                                    value=mainItem["aired"]["string"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Num of Episodes",
                                    value=mainItem["episodes"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Season", value=mainItem["season"], inline=True
                                )
                                .add_field(
                                    name="Year", value=mainItem["year"], inline=True
                                )
                                .add_field(
                                    name="Genres",
                                    value=str(
                                        [items["name"] for items in mainItem["genres"]]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="Themes",
                                    value=str(
                                        [items["name"] for items in mainItem["themes"]]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="MAL URL", value=mainItem["url"], inline=True
                                )
                                .set_image(
                                    url=mainItem["images"]["jpg"]["large_image_url"]
                                )
                                for mainItem in dataMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedVar = discord.Embed()
                    embedVar.description = "Sorry, but the anime you searched for either wasn't found or doesn't exist. Please try again"
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mal.command(name="manga")
    async def manga(self, ctx, *, manga_name: Option(str, "Name of the manga")):
        """Fetches up to 25 mangas from MAL"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"limit": 25, "q": manga_name, "sfw": "true", "order_by": "title"}
            async with session.get(
                "https://api.jikan.moe/v4/manga", params=params
            ) as response:
                data = await response.content.read()
                dataMain2 = parser.parse(data, recursive=True)
                try:
                    if len(dataMain2["data"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=dataItem["title"],
                                    description=dataItem["synopsis"],
                                )
                                .add_field(
                                    name="Japanese Title",
                                    value=dataItem["title_japanese"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Chapters",
                                    value=dataItem["chapters"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Volumes",
                                    value=dataItem["volumes"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Status", value=dataItem["status"], inline=True
                                )
                                .add_field(
                                    name="Published Time",
                                    value=dataItem["published"]["string"],
                                    inline=True,
                                )
                                .add_field(
                                    name="MAL Score",
                                    value=dataItem["score"],
                                    inline=True,
                                )
                                .add_field(
                                    name="MAL Rank", value=dataItem["rank"], inline=True
                                )
                                .add_field(
                                    name="Genres",
                                    value=str(
                                        [items["name"] for items in dataItem["genres"]]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="Themes",
                                    value=str(
                                        [items["name"] for items in dataItem["themes"]]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="MAL URL", value=dataItem["url"], inline=True
                                )
                                .set_image(
                                    url=dataItem["images"]["jpg"]["large_image_url"]
                                )
                                for dataItem in dataMain2["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedVar = discord.Embed()
                    embedVar.description = "Sorry, but it seems like that manga cannot be found. Please try again"
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @malRandom.command(name="anime")
    async def animeRandom(self, ctx):
        """Fetches a random anime from MAL"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.jikan.moe/v4/random/anime") as response:
                data = await response.content.read()
                dataMain = parser.parse(data, recursive=True)
                mainFilter = [
                    "images",
                    "trailer",
                    "aired",
                    "producers",
                    "licensors",
                    "studios",
                    "genres",
                    "explicit_genres",
                    "themes",
                    "demographics",
                    "synopsis",
                    "title",
                    "broadcast",
                    "background",
                ]
                try:
                    if len(dataMain["data"]) == 0:
                        raise ValueError
                    else:
                        embedVar = discord.Embed()
                        embedVar.title = dataMain["data"]["title"]
                        embedVar.description = dataMain["data"]["synopsis"]
                        for key, value in dataMain["data"].items():
                            if key not in mainFilter:
                                embedVar.add_field(
                                    name=str(key).replace("_", " ").capitalize(),
                                    value=value,
                                    inline=True,
                                )
                        embedVar.set_image(
                            url=dataMain["data"]["images"]["jpg"]["large_image_url"]
                        )
                        await ctx.respond(embed=embedVar)

                except ValueError:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "It seems like it might have broke itself... Please try again"
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @malRandom.command(name="manga")
    async def mangaRandom(self, ctx):
        """Fetches a random manga from MAL"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.jikan.moe/v4/random/manga") as r:
                data = await r.content.read()
                dataMain3 = parser.parse(data, recursive=True)
                mangaFilter = [
                    "title",
                    "published",
                    "authors",
                    "serializations",
                    "genres",
                    "explicit_genres",
                    "themes",
                    "demographics",
                    "published",
                    "images",
                    "background",
                    "synopsis",
                ]
                embedVar = discord.Embed()
                try:
                    if len(dataMain3["data"]) == 0:
                        raise ValueError
                    else:
                        embedVar.title = dataMain3["data"]["title"]
                        embedVar.description = dataMain3["data"]["synopsis"]
                        for key, value in dataMain3["data"].items():
                            if key not in mangaFilter:
                                embedVar.add_field(
                                    name=str(key).replace("_", " ").capitalize(),
                                    value=value,
                                    inline=True,
                                )
                        embedVar.set_image(
                            url=dataMain3["data"]["images"]["jpg"]["large_image_url"]
                        )
                        await ctx.respond(embed=embedVar)
                except ValueError:
                    embedVar.description = (
                        "The query could not be done. Please try again"
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @malSeasons.command(name="list")
    async def season(
        self,
        ctx,
        year: Option(int, "Which year for the season"),
        *,
        season: Option(str, "Anime Season - Winter, Spring, Summer or Fall"),
    ):
        """Returns animes for the given season and year"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.jikan.moe/v4/seasons/{year}/{season}"
            ) as response:
                seasons = await response.content.read()
                seasonsMain = parser.parse(seasons, recursive=True)
                try:
                    try:
                        if response.status == 400:
                            raise HTTPException
                        elif len(seasonsMain["data"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=dictItem["title"],
                                        description=dictItem["synopsis"],
                                    )
                                    .set_image(
                                        url=dictItem["images"]["jpg"]["large_image_url"]
                                    )
                                    .add_field(
                                        name="Japanese Title",
                                        value=dictItem["title_japanese"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Similar Titles",
                                        value=dictItem["title_synonyms"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Episodes",
                                        value=dictItem["episodes"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Status",
                                        value=dictItem["status"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Aired",
                                        value=dictItem["aired"]["string"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Score",
                                        value=dictItem["score"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Rank", value=dictItem["rank"], inline=True
                                    )
                                    .add_field(
                                        name="Genres",
                                        value=[
                                            item["name"] for item in dictItem["genres"]
                                        ],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Themes",
                                        value=[
                                            item2["name"]
                                            for item2 in dictItem["themes"]
                                        ],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Demographics",
                                        value=[
                                            item3["name"]
                                            for item3 in dictItem["demographics"]
                                        ],
                                        inline=True,
                                    )
                                    for dictItem in seasonsMain["data"]
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except HTTPException:
                        embedHTTPExceptionError = discord.Embed()
                        embedHTTPExceptionError.description = "It seems like you may have put invalid data, thus causing an error. Please try again, but with the proper data instead"
                        embedHTTPExceptionError.add_field(
                            name="HTTP Code", value=response.status, inline=True
                        )
                        await ctx.respond(embed=embedHTTPExceptionError)
                except NoItemsError:
                    embedNoItemsError = discord.Embed()
                    embedNoItemsError.description = "It seems like there were no items within the database... Please try again"
                    await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @malSeasons.command(name="upcoming")
    async def seasonsUpcoming(self, ctx):
        """Returns anime for the upcoming season"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                "https://api.jikan.moe/v4/seasons/upcoming"
            ) as full_response:
                try:
                    data = await full_response.content.read()
                    dataMain5 = parser.parse(data, recursive=True)
                    mainPages = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=dictItem["title"],
                                description=dictItem["synopsis"],
                            )
                            .set_image(url=dictItem["images"]["jpg"]["large_image_url"])
                            .add_field(name="Aired", value=dictItem["aired"]["string"])
                            .add_field(
                                name="Season", value=dictItem["season"], inline=True
                            )
                            .add_field(
                                name="Japanese Title",
                                value=dictItem["title_japanese"],
                                inline=True,
                            )
                            .add_field(
                                name="Similar Titles",
                                value=dictItem["title_synonyms"],
                                inline=True,
                            )
                            .add_field(
                                name="Rating", value=dictItem["rating"], inline=True
                            )
                            .add_field(
                                name="Episodes", value=dictItem["episodes"], inline=True
                            )
                            .add_field(
                                name="Genres",
                                value=[item["name"] for item in dictItem["genres"]],
                                inline=True,
                            )
                            .add_field(
                                name="Themes",
                                value=[item2["name"] for item2 in dictItem["themes"]],
                                inline=True,
                            )
                            .add_field(
                                name="Demographics",
                                value=[
                                    item3["name"] for item3 in dictItem["demographics"]
                                ],
                                inline=True,
                            )
                            for dictItem in dataMain5["data"]
                        ],
                        loop_pages=True,
                    )
                    await mainPages.respond(ctx.interaction, ephemeral=False)
                except Exception:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Oops, something went wrong. Please try again..."
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mal.command(name="user")
    async def userLookup(self, ctx, *, username: Option(str, "Username of the user")):
        """Returns info about the given user on MAL"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.jikan.moe/v4/users/{username}") as r:
                data = await r.content.read()
                dataMain6 = parser.parse(data, recursive=True)
                userFilter = ["username", "images"]
                try:
                    embedVar = discord.Embed()
                    embedVar.title = dataMain6["data"]["username"]
                    embedVar.set_thumbnail(
                        url=dataMain6["data"]["images"]["jpg"]["image_url"]
                    )
                    for key, value in dataMain6["data"].items():
                        if key not in userFilter:
                            embedVar.add_field(name=key, value=value, inline=True)

                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar.description = (
                        "The query could not be done. Please try again"
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(MALV1(bot))
