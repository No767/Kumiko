import asyncio

import aiohttp
import discord
import orjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands


class JikanV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="jikan-anime",
        description="Fetches up to 5 anime from MAL",
    )
    async def anime(self, ctx, *, anime_name: Option(str, "Name of the anime")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"limit": 5, "q": anime_name,
                      "sfw": "true", "order_by": "title"}
            async with session.get(
                "https://api.jikan.moe/v4/anime/", params=params
            ) as r:
                data = await r.content.read()
                dataMain = orjson.loads(data)
                filterList = [
                    "images",
                    "title",
                    "aired",
                    "synopsis",
                    "background",
                    "broadcast",
                    "producers",
                    "licensors",
                    "studios",
                    "genres",
                    "explicit_genres",
                    "themes",
                    "demographics",
                    "trailer",
                ]
                try:
                    for dictItem in dataMain["data"]:
                        embedVar = discord.Embed()
                        embedVar.title = dictItem["title"]
                        embedVar.description = dictItem["synopsis"]
                        for key, value in dictItem.items():
                            if key not in filterList:
                                embedVar.add_field(
                                    name=str(key).replace(
                                        "_", " ").capitalize(),
                                    value=value,
                                    inline=True,
                                )
                        for item in dictItem["genres"]:
                            embedVar.add_field(
                                name="Genres", value=f'[{item["name"]}]', inline=True
                            )
                        for item2 in dictItem["demographics"]:
                            embedVar.add_field(
                                name="Demographics",
                                value=f'[{item2["name"]}]',
                                inline=True,
                            )
                        for item3 in dictItem["themes"]:
                            embedVar.add_field(
                                name="Themes", value=f'[{item3["name"]}]', inline=True
                            )
                        embedVar.add_field(
                            name="Aired", value=dictItem["aired"]["string"], inline=True
                        )
                        embedVar.set_image(
                            url=dictItem["images"]["jpg"]["large_image_url"]
                        )
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "The query could not be done. Please try again"
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class JikanV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="jikan-manga",
        description="Fetches up to 5 mangas from MAL",
    )
    async def manga(self, ctx, *, manga_name: Option(str, "Name of the manga")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"limit": 5, "q": manga_name,
                      "sfw": "true", "order_by": "title"}
            async with session.get(
                "https://api.jikan.moe/v4/manga", params=params
            ) as response:
                data = await response.content.read()
                dataMain2 = orjson.loads(data)
                filterList = [
                    "title",
                    "images",
                    "published",
                    "authors",
                    "serializations",
                    "genres",
                    "explicit_genres",
                    "themes",
                    "demographics",
                    "background",
                    "synopsis",
                ]
                try:
                    for dataItem in dataMain2["data"]:
                        embedVar = discord.Embed()
                        embedVar.title = dataItem["title"]
                        embedVar.description = dataItem["synopsis"]
                        embedVar.set_image(
                            url=dataItem["images"]["jpg"]["large_image_url"]
                        )
                        for key, value in dataItem.items():
                            if key not in filterList:
                                embedVar.add_field(
                                    name=str(key).replace(
                                        "_", " ").capitalize(),
                                    value=value,
                                    inline=True,
                                )
                        for name in dataItem["authors"]:
                            embedVar.add_field(
                                name="Authors", value=f'[{name["name"]}]', inline=True
                            )
                        for obj in dataItem["serializations"]:
                            embedVar.add_field(
                                name="Serializations",
                                value=f'[{obj["name"]}]',
                                inline=True,
                            )
                        for genre in dataItem["genres"]:
                            embedVar.add_field(
                                name="Genres", value=f'[{genre["name"]}]', inline=True
                            )
                        for theme in dataItem["themes"]:
                            embedVar.add_field(
                                name="Themes", value=f'[{theme["name"]}]', inline=True
                            )
                        for demographic in dataItem["demographics"]:
                            embedVar.add_field(
                                name="Demographics",
                                value=f'[{demographic["name"]}]',
                                inline=True,
                            )
                        embedVar.add_field(
                            name="Published",
                            value=dataItem["published"]["string"],
                            inline=True,
                        )
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "The query could not be done. Please try again"
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class JikanV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="jikan-random-anime",
        description="Fetches a random anime from MAL",
    )
    async def animeRandom(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.jikan.moe/v4/random/anime") as response:
                data = await response.json()
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
                    embedVar = discord.Embed()
                    embedVar.title = data["data"]["title"]
                    embedVar.description = data["data"]["synopsis"]
                    for key, value in data["data"].items():
                        if key not in mainFilter:
                            embedVar.add_field(
                                name=str(key).replace("_", " ").capitalize(),
                                value=value,
                                inline=True,
                            )
                    embedVar.set_image(
                        url=data["data"]["images"]["jpg"]["large_image_url"]
                    )
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "The query could not be done. Please try again"
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)


class JikanV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="jikan-random-manga",
        description="Fetches a random manga from MAL",
    )
    async def mangaRandom(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.jikan.moe/v4/random/manga") as r:
                data = await r.content.read()
                dataMain3 = orjson.loads(data)
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
                except Exception as e:
                    embedVar.description = (
                        "The query could not be done. Please try again"
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)


class JikanV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="jikan-seasons",
        description="Returns animes for the given season and year",
    )
    async def season(
        self,
        ctx,
        year: Option(int, "Which year for the season"),
        *,
        season: Option(str, "Anime Season - Winter, Spring, Summer or Fall"),
    ):
        if season in ["winter", "spring", "summer", "fall"]:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                async with session.get(
                    f"https://api.jikan.moe/v4/seasons/{year}/{season}"
                ) as response:
                    seasons = await response.content.read()
                    seasonsMain = orjson.loads(seasons)
                    mainSeasonsFilter = [
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
                        "title",
                        "synopsis",
                        "background",
                        "broadcast",
                    ]
                    embedVar = discord.Embed()
                    for dictItem in seasonsMain["data"]:
                        embedVar.title = dictItem["title"]
                        embedVar.description = dictItem["synopsis"]
                        for k, v in dictItem.items():
                            if k not in mainSeasonsFilter:
                                embedVar.add_field(
                                    name=str(k).replace("_", " ").capitalize(),
                                    value=v,
                                    inline=True,
                                )
                        for item in dictItem["genres"]:
                            embedVar.add_field(
                                name="Genres", value=item["name"], inline=True
                            )
                        for item1 in dictItem["themes"]:
                            embedVar.add_field(
                                name="Themes", value=item1["name"], inline=True
                            )
                        for item2 in dictItem["demographics"]:
                            embedVar.add_field(
                                name="Demographics", value=item2["name"], inline=True
                            )
                        embedVar.set_image(
                            url=dictItem["images"]["jpg"]["large_image_url"]
                        )
                        await ctx.respond(embed=embedVar)


class JikanV6(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="jikan-season-upcoming",
        description="Returns anime for the upcoming season (will return ALL of it)",
    )
    async def seasonsUpcoming(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                "https://api.jikan.moe/v4/seasons/upcoming"
            ) as full_response:
                data = await full_response.content.read()
                dataMain5 = orjson.loads(data)
                mainFilter = [
                    "broadcast",
                    "title",
                    "synopsis",
                    "images",
                    "trailer",
                    "producers",
                    "licensors",
                    "studios",
                    "genres",
                    "explicit_genres",
                    "themes",
                    "demographics",
                    "broadcast",
                    "aired",
                ]
                for dictItem in dataMain5["data"]:
                    embedVar = discord.Embed()
                    embedVar.title = dictItem["title"]
                    embedVar.description = dictItem["synopsis"]
                    embedVar.set_image(
                        url=dictItem["images"]["jpg"]["large_image_url"])
                    embedVar.add_field(
                        name="Aired", value=dictItem["aired"]["string"], inline=True
                    )
                    for key, value in dictItem.items():
                        if key not in mainFilter:
                            embedVar.add_field(
                                name=str(key).replace("_", " ").capitalize(),
                                value=value,
                                inline=True,
                            )
                    await ctx.respond(embed=embedVar)


class JikanV7(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="jikan-user-profile",
        description="Returns info about given user on MAL",
    )
    async def userLookup(self, ctx, *, username: Option(str, "Username of the user")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.jikan.moe/v4/users/{username}") as r:
                data = await r.content.read()
                dataMain6 = orjson.loads(data)
                userFilter = ["username", "images"]
                try:
                    embedVar = discord.Embed()
                    embedVar.title = dataMain6["data"]["username"]
                    embedVar.set_thumbnail(
                        url=dataMain6["data"]["images"]["jpg"]["image_url"]
                    )
                    for key, value in dataMain6["data"].items():
                        if key not in userFilter:
                            embedVar.add_field(
                                name=key, value=value, inline=True)

                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar.description = (
                        "The query could not be done. Please try again"
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)


def setup(bot):
    bot.add_cog(JikanV1(bot))
    bot.add_cog(JikanV2(bot))
    bot.add_cog(JikanV3(bot))
    bot.add_cog(JikanV4(bot))
    # bot.add_cog(JikanV5(bot)) # Disabled due to spam issues...
    # bot.add_cog(JikanV6(bot))
    bot.add_cog(JikanV7(bot))
