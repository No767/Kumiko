import asyncio

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands


class JikanV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-anime", aliases=["jk-anime"])
    async def anime(self, ctx, *, search: str):
        search = search.replace(" ", "%20")
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"q": search, "order_by": "title", "limit": 1}
            async with session.get(
                "https://api.jikan.moe/v3/search/anime", params=params
            ) as r:
                data = await r.json()
                anime_id = data["results"][0]["mal_id"]
                async with session.get(
                    f"https://api.jikan.moe/v3/anime/{anime_id}"
                ) as resp:
                    anime_info_v2 = await resp.json()
                    print(anime_info_v2)
                    try:
                        embedVar = discord.Embed(title=anime_info_v2["title"])
                        embedVar2 = discord.Embed(
                            title=f"Synopsis - {anime_info_v2['title_english']}"
                        )
                        embedVar.add_field(
                            name="English Title",
                            value=anime_info_v2["title_english"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Japanese Title",
                            value=anime_info_v2["title_japanese"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Title Synonyms",
                            value=str(anime_info_v2["title_synonyms"]).replace(
                                "'", ""),
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Type", value=anime_info_v2["type"], inline=True
                        )
                        embedVar.add_field(
                            name="Source", value=anime_info_v2["source"], inline=True
                        )
                        embedVar.add_field(
                            name="Status", value=anime_info_v2["status"], inline=True
                        )
                        embedVar.add_field(
                            name="Aired",
                            value=anime_info_v2["aired"]["string"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Premiered",
                            value=anime_info_v2["premiered"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Rating", value=anime_info_v2["rating"], inline=True
                        )
                        embedVar.add_field(
                            name="Score", value=anime_info_v2["score"], inline=True
                        )
                        embedVar.add_field(
                            name="Scored By",
                            value=anime_info_v2["scored_by"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Rank", value=anime_info_v2["rank"], inline=True
                        )
                        embedVar.add_field(
                            name="Popularity",
                            value=anime_info_v2["popularity"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Members", value=anime_info_v2["members"], inline=True
                        )
                        embedVar.add_field(
                            name="Favorites",
                            value=anime_info_v2["favorites"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Official Site",
                            value=anime_info_v2["external_links"][0]["url"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="AnimeDB",
                            value=anime_info_v2["external_links"][1]["url"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="AnimeNewsNetwork",
                            value=anime_info_v2["external_links"][2]["url"],
                            inline=True,
                        )
                        embedVar2.description = f"{str(anime_info_v2['synopsis']).replace('[Written by MAL Rewrite]', '')}"
                        embedVar2.add_field(
                            name="Background",
                            value=anime_info_v2["background"],
                            inline=True,
                        )
                        embedVar.set_thumbnail(url=anime_info_v2["image_url"])
                        await ctx.send(embed=embedVar)
                        await ctx.send(embed=embedVar2)
                    except Exception as e:
                        embedVar = discord.Embed()
                        embedVar.description = f"The query could not be performed. Please try again.\nReason: {e}"
                        await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @anime.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = "Missing a required argument: Anime name"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class JikanV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-manga", aliases=["jk-manga"])
    async def manga(self, ctx, *, search: str):
        search = search.replace(" ", "%20")
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"q": search}
            async with session.get(
                "https://api.jikan.moe/v3/search/manga", params=params
            ) as response:
                data = await response.json()
                manga_id = data["results"][0]["mal_id"]
                async with session.get(
                    f"https://api.jikan.moe/v3/manga/{manga_id}"
                ) as re:
                    manga_info_v1 = await re.json()
                    print(manga_info_v1)
                    try:
                        embedVar = discord.Embed(
                            title=manga_info_v1["title"],
                            color=discord.Color.from_rgb(145, 197, 255),
                        )
                        embedVar2 = discord.Embed(
                            title=f"Synopsis - {manga_info_v1['title']}",
                            color=discord.Color.from_rgb(145, 197, 255),
                        )
                        embedVar.add_field(
                            name="English Title",
                            value=manga_info_v1["title_english"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Japanese Title",
                            value=manga_info_v1["title_japanese"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Title Synonyms",
                            value=str(manga_info_v1["title_synonyms"]).replace(
                                "'", ""),
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Status", value=manga_info_v1["status"], inline=True
                        )
                        embedVar.add_field(
                            name="Type", value=manga_info_v1["type"], inline=True
                        )
                        embedVar.add_field(
                            name="Published",
                            value=manga_info_v1["publishing"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Published Status",
                            value=manga_info_v1["published"]["string"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Volumes", value=manga_info_v1["volumes"], inline=True
                        )
                        embedVar.add_field(
                            name="Chapters",
                            value=manga_info_v1["chapters"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Genre",
                            value=str(
                                [name["name"]
                                    for name in manga_info_v1["genres"]]
                            )
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", ""),
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Author(s)",
                            value=str(
                                [name["name"]
                                    for name in manga_info_v1["authors"]]
                            )
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", ""),
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Rank", value=manga_info_v1["rank"], inline=True
                        )
                        embedVar.add_field(
                            name="Score", value=manga_info_v1["score"], inline=True
                        )
                        embedVar.add_field(
                            name="Scored by",
                            value=manga_info_v1["scored_by"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Popularity",
                            value=manga_info_v1["popularity"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Members", value=manga_info_v1["members"], inline=True
                        )
                        embedVar.add_field(
                            name="Favorites",
                            value=manga_info_v1["favorites"],
                            inline=True,
                        )
                        embedVar2.description = f"{manga_info_v1['synopsis']}"
                        embedVar2.add_field(
                            name="Background",
                            value=manga_info_v1["background"],
                            inline=True,
                        )
                        embedVar.set_thumbnail(url=manga_info_v1["image_url"])
                        await ctx.send(embed=embedVar)
                        await ctx.send(embed=embedVar2)
                    except Exception as e:
                        embedVar = discord.Embed(
                            color=discord.Color.from_rgb(235, 201, 255)
                        )
                        embedVar.description = f"The current query could not be performed. Please try again.\nReason: {e}"
                        await ctx.send(emvbed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @manga.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = "Missing a required argument: Manga name"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class JikanV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-top", aliases=["jk-top"])
    async def top(self, ctx, *, type: str):
        try:
            if str(type) in "anime":
                async with aiohttp.ClientSession(
                    json_serialize=orjson.dumps
                ) as session:
                    async with session.get(
                        f"https://api.jikan.moe/v3/top/{type}"
                    ) as res:
                        top_items = await res.json()
                        embedVar = discord.Embed(
                            title="Top 10 Anime",
                            color=discord.Color.from_rgb(219, 166, 255),
                        )
                        embedVar.add_field(
                            name="Top 1",
                            value=top_items["top"][0]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 2",
                            value=top_items["top"][1]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 3",
                            value=top_items["top"][2]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 4",
                            value=top_items["top"][3]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 5",
                            value=top_items["top"][4]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 6",
                            value=top_items["top"][5]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 7",
                            value=top_items["top"][6]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 8",
                            value=top_items["top"][7]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 9",
                            value=top_items["top"][8]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 10",
                            value=top_items["top"][9]["title"],
                            inline=True,
                        )
                        await ctx.send(embed=embedVar)
            if str(type) in "manga":
                async with aiohttp.ClientSession(
                    json_serialize=orjson.dumps
                ) as session:
                    async with session.get(
                        f"https://api.jikan.moe/v3/top/{type}"
                    ) as respo:
                        top_items = await respo.json()
                        embedVar = discord.Embed(
                            title="Top 10 Manga",
                            color=discord.Color.from_rgb(166, 225, 255),
                        )
                        embedVar.add_field(
                            name="Top 1",
                            value=top_items["top"][0]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 2",
                            value=top_items["top"][1]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 3",
                            value=top_items["top"][2]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 4",
                            value=top_items["top"][3]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 5",
                            value=top_items["top"][4]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 6",
                            value=top_items["top"][5]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 7",
                            value=top_items["top"][6]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 8",
                            value=top_items["top"][7]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 9",
                            value=top_items["top"][8]["title"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 10",
                            value=top_items["top"][9]["title"],
                            inline=True,
                        )
                        await ctx.send(embed=embedVar)
            if str(type) in "people":
                async with aiohttp.ClientSession(
                    json_serialize=orjson.dumps
                ) as session:
                    async with session.get(
                        f"https://api.jikan.moe/v3/top/{type}"
                    ) as ree:
                        top_items = await ree.json()
                        embedVar = discord.Embed(
                            title="Top 10 Voice Actors",
                            color=discord.Color.from_rgb(255, 201, 248),
                        )
                        embedVar.add_field(
                            name="Top 1",
                            value=f"{top_items['top'][0]['title']} ({top_items['top'][0]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 2",
                            value=f"{top_items['top'][1]['title']} ({top_items['top'][1]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 3",
                            value=f"{top_items['top'][2]['title']} ({top_items['top'][2]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 4",
                            value=f"{top_items['top'][3]['title']} ({top_items['top'][3]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 5",
                            value=f"{top_items['top'][4]['title']} ({top_items['top'][4]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 6",
                            value=f"{top_items['top'][5]['title']} ({top_items['top'][5]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 7",
                            value=f"{top_items['top'][6]['title']} ({top_items['top'][6]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 8",
                            value=f"{top_items['top'][7]['title']} ({top_items['top'][7]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 9",
                            value=f"{top_items['top'][8]['title']} ({top_items['top'][8]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 10",
                            value=f"{top_items['top'][9]['title']} ({top_items['top'][9]['name_kanji']})",
                            inline=True,
                        )
                        await ctx.send(embed=embedVar)
            if str(type) in "characters":
                async with aiohttp.ClientSession(
                    json_serialize=orjson.dumps
                ) as session:
                    async with session.get(
                        f"https://api.jikan.moe/v3/top/{type}"
                    ) as a_response:
                        top_items = await a_response.json()
                        embedVar = discord.Embed(
                            title="Top 10 Characters",
                            color=discord.Color.from_rgb(255, 249, 201),
                        )
                        embedVar.add_field(
                            name="Top 1",
                            value=f"{top_items['top'][0]['title']} ({top_items['top'][0]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 2",
                            value=f"{top_items['top'][1]['title']} ({top_items['top'][1]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 3",
                            value=f"{top_items['top'][2]['title']} ({top_items['top'][2]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 4",
                            value=f"{top_items['top'][3]['title']} ({top_items['top'][3]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 5",
                            value=f"{top_items['top'][4]['title']} ({top_items['top'][4]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 6",
                            value=f"{top_items['top'][5]['title']} ({top_items['top'][5]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 7",
                            value=f"{top_items['top'][6]['title']} ({top_items['top'][6]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 8",
                            value=f"{top_items['top'][7]['title']} ({top_items['top'][7]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 9",
                            value=f"{top_items['top'][8]['title']} ({top_items['top'][8]['name_kanji']})",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Top 10",
                            value=f"{top_items['top'][9]['title']} ({top_items['top'][9]['name_kanji']})",
                            inline=True,
                        )
                        await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(235, 201, 255))
            embedVar.description = f"The current query could not be performed. Please try again.\nReason: {e}"
            await ctx.send(emvbed=embedVar)

    @top.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}\nThese are the following: `anime`, `manga`, `characters`, `people`"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class JikanV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-season", aliases=["jk-season"])
    async def season(self, ctx, year: int, *, season: str):
        try:
            if str(season) in ["winter", "spring", "summer", "fall"]:
                async with aiohttp.ClientSession(
                    json_serialize=orjson.dumps
                ) as session:
                    async with session.get(
                        f"https://api.jikan.moe/v3/season/{year}/{season}"
                    ) as response:
                        seasonv1 = await response.json()
                        embedVar = discord.Embed(
                            title=f"{seasonv1['season_year']} {seasonv1['season_name']} Animes [Anime 1]",
                            color=discord.Color.from_rgb(255, 249, 201),
                        )
                        embedVar.add_field(
                            name="Name",
                            value=f"{seasonv1['anime'][0]['title']}",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Episodes",
                            value=f"{seasonv1['anime'][0]['episodes']}",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Genre(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][0]["genres"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Theme(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][0]["themes"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Continuing",
                            value=f"{seasonv1['anime'][0]['continuing']}",
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Score",
                            value=f"{seasonv1['anime'][0]['score']}",
                            inline=True,
                        )
                        embedVar.set_thumbnail(
                            url=seasonv1["anime"][0]["image_url"])
                        embedVar2 = discord.Embed(
                            title=f"{seasonv1['season_year']} {seasonv1['season_name']} Animes [Anime 2]",
                            color=discord.Color.from_rgb(66, 188, 245),
                        )
                        embedVar2.add_field(
                            name="Name",
                            value=f"{seasonv1['anime'][1]['title']}",
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Episodes",
                            value=f"{seasonv1['anime'][1]['episodes']}",
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Genre(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][1]["genres"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Theme(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][1]["themes"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Continuing",
                            value=f"{seasonv1['anime'][1]['continuing']}",
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Score",
                            value=f"{seasonv1['anime'][1]['score']}",
                            inline=True,
                        )
                        embedVar2.set_thumbnail(
                            url=seasonv1["anime"][1]["image_url"])
                        embedVar3 = discord.Embed(
                            title=f"{seasonv1['season_year']} {seasonv1['season_name']} Animes [Anime 3]",
                            color=discord.Color.from_rgb(245, 185, 66),
                        )
                        embedVar3.add_field(
                            name="Name",
                            value=f"{seasonv1['anime'][2]['title']}",
                            inline=True,
                        )
                        embedVar3.add_field(
                            name="Episodes",
                            value=f"{seasonv1['anime'][2]['episodes']}",
                            inline=True,
                        )
                        embedVar3.add_field(
                            name="Genre(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][2]["genres"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar3.add_field(
                            name="Theme(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][2]["themes"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar3.add_field(
                            name="Continuing",
                            value=f"{seasonv1['anime'][2]['continuing']}",
                            inline=True,
                        )
                        embedVar3.add_field(
                            name="Score",
                            value=f"{seasonv1['anime'][2]['score']}",
                            inline=True,
                        )
                        embedVar3.set_thumbnail(
                            url=seasonv1["anime"][2]["image_url"])
                        embedVar4 = discord.Embed(
                            title=f"{seasonv1['season_year']} {seasonv1['season_name']} Animes [Anime 4]",
                            color=discord.Color.from_rgb(255, 206, 173),
                        )
                        embedVar4.add_field(
                            name="Name",
                            value=f"{seasonv1['anime'][3]['title']}",
                            inline=True,
                        )
                        embedVar4.add_field(
                            name="Episodes",
                            value=f"{seasonv1['anime'][3]['episodes']}",
                            inline=True,
                        )
                        embedVar4.add_field(
                            name="Genre(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][3]["genres"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar4.add_field(
                            name="Theme(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][3]["themes"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar4.add_field(
                            name="Continuing",
                            value=seasonv1["anime"][3]["continuing"],
                            inline=True,
                        )
                        embedVar4.add_field(
                            name="Score",
                            value=seasonv1["anime"][3]["score"],
                            inline=True,
                        )
                        embedVar4.set_thumbnail(
                            url=seasonv1["anime"][3]["image_url"])
                        embedVar5 = discord.Embed(
                            title=f"{seasonv1['season_year']} {seasonv1['season_name']} Animes [Anime 5]",
                            color=discord.Color.from_rgb(255, 173, 224),
                        )
                        embedVar5.add_field(
                            name="Name",
                            value=f"{seasonv1['anime'][4]['title']}",
                            inline=True,
                        )
                        embedVar5.add_field(
                            name="Episodes",
                            value=f"{seasonv1['anime'][4]['episodes']}",
                            inline=True,
                        )
                        embedVar5.add_field(
                            name="Genre(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][4]["genres"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar5.add_field(
                            name="Theme(s)",
                            value=str(
                                [
                                    name["name"]
                                    for name in seasonv1["anime"][4]["themes"]
                                ]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embedVar5.add_field(
                            name="Continuing",
                            value=seasonv1["anime"][4]["continuing"],
                            inline=True,
                        )
                        embedVar5.add_field(
                            name="Score",
                            value=seasonv1["anime"][4]["score"],
                            inline=True,
                        )
                        embedVar5.set_thumbnail(
                            url=seasonv1["anime"][4]["image_url"])
                        await ctx.send(embed=embedVar)
                        await ctx.send(embed=embedVar2)
                        await ctx.send(embed=embedVar3)
                        await ctx.send(embed=embedVar4)
                        await ctx.send(embed=embedVar5)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(235, 201, 255))
            embedVar.description = f"The current query could not be performed. Please try again.\nReason: {e}"
            await ctx.send(embed=embedVar)

    @season.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}\n\nFor selecting a year, it can be from 1917-present.\nFor selecting which season, you must provide only one of these: `spring`, `fall`, `winter`, `summer`."
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class JikanV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-season-later", aliases=["jk-season-later"])
    async def on_message(self, ctx):
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                async with session.get(
                    "https://api.jikan.moe/v3/season/later"
                ) as full_response:
                    season_later = await full_response.json()
                    embedVar = discord.Embed(
                        title=f"{season_later['season_name']} Animes [Anime 1]",
                        color=discord.Color.from_rgb(255, 252, 171),
                    )
                    embedVar.add_field(
                        name="Name",
                        value=f"{season_later['anime'][0]['title']}",
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Synopsis",
                        value=f"{season_later['anime'][0]['synopsis']}".replace(
                            "[Written by MAL Rewrite]", ""
                        ),
                        inline=False,
                    )
                    embedVar.add_field(
                        name="Genre(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][0]["genres"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Theme(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][0]["themes"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Continuing",
                        value=season_later["anime"][0]["continuing"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="MAL ID",
                        value=season_later["anime"][0]["mal_id"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Source",
                        value=season_later["anime"][0]["source"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Type", value=season_later["anime"][0]["type"], inline=True
                    )
                    embedVar.set_thumbnail(
                        url=season_later["anime"][0]["image_url"])
                    embedVar2 = discord.Embed(
                        title=f"{season_later['season_name']} Animes [Anime 2]",
                        color=discord.Color.from_rgb(219, 255, 171),
                    )
                    embedVar2.add_field(
                        name="Name",
                        value=f"{season_later['anime'][1]['title']}",
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Synopsis",
                        value=f"{season_later['anime'][1]['synopsis']}".replace(
                            "[Written by MAL Rewrite]", ""
                        ),
                        inline=False,
                    )
                    embedVar2.add_field(
                        name="Genre(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][1]["genres"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Theme(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][1]["themes"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Continuing",
                        value=season_later["anime"][1]["continuing"],
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="MAL ID",
                        value=season_later["anime"][1]["mal_id"],
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Source",
                        value=season_later["anime"][1]["source"],
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Type", value=season_later["anime"][1]["type"], inline=True
                    )
                    embedVar2.set_thumbnail(
                        url=season_later["anime"][1]["image_url"])
                    embedVar3 = discord.Embed(
                        title=f"{season_later['season_name']} Animes [Anime 3]",
                        color=discord.Color.from_rgb(171, 255, 193),
                    )
                    embedVar3.add_field(
                        name="Name",
                        value=f"{season_later['anime'][2]['title']}",
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Synopsis",
                        value=f"{season_later['anime'][2]['synopsis']}".replace(
                            "[Written by MAL Rewrite]", ""
                        ),
                        inline=False,
                    )
                    embedVar3.add_field(
                        name="Genre(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][2]["genres"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Theme(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][2]["themes"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Continuing",
                        value=season_later["anime"][2]["continuing"],
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="MAL ID",
                        value=season_later["anime"][2]["mal_id"],
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Source",
                        value=season_later["anime"][2]["source"],
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Type", value=season_later["anime"][2]["type"], inline=True
                    )
                    embedVar3.set_thumbnail(
                        url=season_later["anime"][2]["image_url"])
                    embedVar4 = discord.Embed(
                        title=f"{season_later['season_name']} Animes [Anime 4]",
                        color=discord.Color.from_rgb(171, 255, 237),
                    )
                    embedVar4.add_field(
                        name="Name",
                        value=f"{season_later['anime'][3]['title']}",
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Synopsis",
                        value=f"{season_later['anime'][3]['synopsis']}".replace(
                            "[Written by MAL Rewrite]", ""
                        ),
                        inline=False,
                    )
                    embedVar4.add_field(
                        name="Genre(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][3]["genres"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Theme(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][3]["themes"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Continuing",
                        value=season_later["anime"][3]["continuing"],
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="MAL ID",
                        value=season_later["anime"][3]["mal_id"],
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Source",
                        value=season_later["anime"][3]["source"],
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Type", value=season_later["anime"][3]["type"], inline=True
                    )
                    embedVar4.set_thumbnail(
                        url=season_later["anime"][3]["image_url"])
                    embedVar5 = discord.Embed(
                        title=f"{season_later['season_name']} Animes [Anime 5]",
                        color=discord.Color.from_rgb(171, 231, 255),
                    )
                    embedVar5.add_field(
                        name="Name",
                        value=f"{season_later['anime'][4]['title']}",
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Synopsis",
                        value=f"{season_later['anime'][4]['synopsis']}".replace(
                            "[Written by MAL Rewrite]", ""
                        ),
                        inline=False,
                    )
                    embedVar5.add_field(
                        name="Genre(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][4]["genres"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Theme(s)",
                        value=str(
                            [
                                name["name"]
                                for name in season_later["anime"][4]["themes"]
                            ]
                        ).replace("'", ""),
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Continuing",
                        value=season_later["anime"][4]["continuing"],
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="MAL ID",
                        value=season_later["anime"][4]["mal_id"],
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Source",
                        value=season_later["anime"][4]["source"],
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Type", value=season_later["anime"][4]["type"], inline=True
                    )
                    embedVar5.set_thumbnail(
                        url=season_later["anime"][4]["image_url"])
                    await ctx.send(embed=embedVar)
                    await ctx.send(embed=embedVar2)
                    await ctx.send(embed=embedVar3)
                    await ctx.send(embed=embedVar4)
                    await ctx.send(embed=embedVar5)

        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(235, 201, 255))
            embedVar.description = f"The current query could not be performed. Please try again.\nReason: {e}"
            await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(JikanV1(bot))
    bot.add_cog(JikanV2(bot))
    bot.add_cog(JikanV3(bot))
    bot.add_cog(JikanV4(bot))
    bot.add_cog(JikanV5(bot))
