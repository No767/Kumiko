import discord
import requests
import ujson
from discord.ext import commands


def get_anime_info(search):
    search = search.replace(" ", "%20")
    link = f"https://api.jikan.moe/v3/search/anime?q={search}"
    r = requests.get(link)
    anime_info = ujson.loads(r.text)
    return anime_info


def search_manga_info(search):
    search = search.replace(" ", "%20")
    link = f"https://api.jikan.moe/v3/search/manga?q={search}"
    r = requests.get(link)
    manga_info = ujson.loads(r.text)
    return manga_info


def get_related_anime_info_pictures(id):
    link = f"https://api.jikan.moe/v3/anime/{id}/pictures"
    r = requests.get(link)
    return ujson.loads(r.text)


def get_anime_infov2(id):
    link = f"https://api.jikan.moe/v3/anime/{id}"
    r = requests.get(link)
    anime_info_v2 = ujson.loads(r.text)
    return anime_info_v2


def get_manga_info(id):
    link = f"https://api.jikan.moe/v3/manga/{id}"
    r = requests.get(link)
    manga_info = ujson.loads(r.text)
    return manga_info


def get_top_items(type):
    link = f"https://api.jikan.moe/v3/top/{type}"
    r = requests.get(link)
    top_items = ujson.loads(r.text)
    return top_items


def get_season(year, season):
    link = f"https://api.jikan.moe/v3/season/{year}/{season}"
    r = requests.get(link)
    season_info = ujson.loads(r.text)
    return season_info


class JikanV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-anime")
    async def anime(self, ctx, *, search: str):
        anime_info = get_anime_info(search)
        id = anime_info["results"][0]["mal_id"]
        anime_info_v2 = get_anime_infov2(id)
        try:
            embedVar = discord.Embed(title=anime_info_v2["title"])
            embedVar.add_field(
                name="English Title", value=anime_info_v2["title_english"], inline=False
            )
            embedVar.add_field(
                name="Japanese Title",
                value=anime_info_v2["title_japanese"],
                inline=False,
            )
            embedVar.add_field(
                name="Title Synonyms",
                value=str(anime_info_v2["title_synonyms"])
                .replace("[", "")
                .replace("]", "")
                .replace("'", ""),
                inline=False,
            )
            embedVar.add_field(
                name="Synopsis",
                value=str(anime_info_v2["synopsis"]).replace(
                    "[Written by MAL Rewrite]", ""
                ),
                inline=False,
            )
            embedVar.add_field(
                name="Background", value=anime_info_v2["background"], inline=True
            )
            embedVar.add_field(
                name="Type", value=anime_info_v2["type"], inline=True)
            embedVar.add_field(
                name="Source", value=anime_info_v2["source"], inline=True
            )
            embedVar.add_field(
                name="Status", value=anime_info_v2["status"], inline=True
            )
            embedVar.add_field(
                name="Aired", value=anime_info_v2["aired"]["string"], inline=True
            )
            embedVar.add_field(
                name="Premiered", value=anime_info_v2["premiered"], inline=True
            )
            embedVar.add_field(
                name="Rating", value=anime_info_v2["rating"], inline=True
            )
            embedVar.add_field(
                name="Score", value=anime_info_v2["score"], inline=True)
            embedVar.add_field(
                name="Scored By", value=anime_info_v2["scored_by"], inline=True
            )
            embedVar.add_field(
                name="Rank", value=anime_info_v2["rank"], inline=True)
            embedVar.add_field(
                name="Popularity", value=anime_info_v2["popularity"], inline=True
            )
            embedVar.add_field(
                name="Members", value=anime_info_v2["members"], inline=True
            )
            embedVar.add_field(
                name="Favorites", value=anime_info_v2["favorites"], inline=True
            )
            embedVar.set_thumbnail(url=anime_info_v2["image_url"])
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed()
            embedVar.description = (
                f"The query could not be performed. Please try again.\nReason: {e}"
            )
            await ctx.send(embed=embedVar)


class JikanV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-manga")
    async def manga(self, ctx, *, search: str):
        more_manga_info = search_manga_info(search)
        id = more_manga_info["results"][0]["mal_id"]
        manga_info_v1 = get_manga_info(id)
        try:
            embedVar = discord.Embed(
                title=manga_info_v1["title"],
                color=discord.Color.from_rgb(145, 197, 255),
            )
            embedVar.add_field(
                name="English Title", value=manga_info_v1["title_english"], inline=True
            )
            embedVar.add_field(
                name="Japanese Title",
                value=manga_info_v1["title_japanese"],
                inline=True,
            )
            embedVar.add_field(
                name="Title Synonyms",
                value=str(manga_info_v1["title_synonyms"])
                .replace("[", "")
                .replace("]", "")
                .replace("'", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Synopsis", value=manga_info_v1["synopsis"], inline=True
            )
            embedVar.add_field(
                name="Background", value=manga_info_v1["background"], inline=True
            )
            embedVar.add_field(
                name="Status", value=manga_info_v1["status"], inline=True
            )
            embedVar.add_field(
                name="Type", value=manga_info_v1["type"], inline=True)
            embedVar.add_field(
                name="Published", value=manga_info_v1["publishing"], inline=True
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
                name="Chapters", value=manga_info_v1["chapters"], inline=True
            )
            embedVar.add_field(
                name="Genre",
                value=str([name["name"] for name in manga_info_v1["genres"]])
                .replace("[", "")
                .replace("]", "")
                .replace("'", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Demographics",
                value=str([name["name"]
                          for name in manga_info_v1["demographics"]])
                .replace("[", "")
                .replace("]", "")
                .replace("'", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Themes",
                value=str([name["name"] for name in manga_info_v1["themes"]])
                .replace("[", "")
                .replace("]", "")
                .replace("'", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Author(s)",
                value=str([name["name"] for name in manga_info_v1["authors"]])
                .replace("[", "")
                .replace("]", "")
                .replace("'", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Rank", value=manga_info_v1["rank"], inline=True)
            embedVar.add_field(
                name="Score", value=manga_info_v1["score"], inline=True)
            embedVar.add_field(
                name="Scored by", value=manga_info_v1["scored_by"], inline=True
            )
            embedVar.add_field(
                name="Popularity", value=manga_info_v1["popularity"], inline=True
            )
            embedVar.add_field(
                name="Members", value=manga_info_v1["members"], inline=True
            )
            embedVar.add_field(
                name="Favorites", value=manga_info_v1["favorites"], inline=True
            )
            embedVar.set_thumbnail(url=manga_info_v1["image_url"])
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(235, 201, 255))
            embedVar.description = f"The current query could not be performed. Please try again.\nReason: {e}"
            await ctx.send(emvbed=embedVar)


class JikanV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-top")
    async def top(self, ctx, *, type: str):
        try:
            if str(type) in "anime":
                top_items = get_top_items(type)
                embedVar = discord.Embed(
                    title="Top 10 Anime", color=discord.Color.from_rgb(219, 166, 255)
                )
                embedVar.add_field(
                    name=f"Top 1", value=top_items["top"][0]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 2", value=top_items["top"][1]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 3", value=top_items["top"][2]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 4", value=top_items["top"][3]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 5", value=top_items["top"][4]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 6", value=top_items["top"][5]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 7", value=top_items["top"][6]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 8", value=top_items["top"][7]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 9", value=top_items["top"][8]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 10", value=top_items["top"][9]["title"], inline=True
                )
                await ctx.send(embed=embedVar)
            if str(type) in "manga":
                top_items = get_top_items(type)
                embedVar = discord.Embed(
                    title="Top 10 Manga", color=discord.Color.from_rgb(166, 225, 255)
                )
                embedVar.add_field(
                    name=f"Top 1", value=top_items["top"][0]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 2", value=top_items["top"][1]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 3", value=top_items["top"][2]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 4", value=top_items["top"][3]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 5", value=top_items["top"][4]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 6", value=top_items["top"][5]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 7", value=top_items["top"][6]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 8", value=top_items["top"][7]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 9", value=top_items["top"][8]["title"], inline=True
                )
                embedVar.add_field(
                    name=f"Top 10", value=top_items["top"][9]["title"], inline=True
                )
                await ctx.send(embed=embedVar)
            if str(type) in "people":
                top_items = get_top_items(type)
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
                top_items = get_top_items(type)
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


class JikanV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jikan-season")
    async def on_message(self, ctx, year: int, *, season: str):
        try:
            seasonv1 = get_season(year, season)  # Fix this tmmr
            embedVar = discord.Embed(
                title=f"{year} {season} Animes",
                color=discord.Color.from_rgb(255, 249, 201),
            )
            embedVar.add_field(
                name="Name", value=f"{seasonv1['anime'][0]['title']}", inline=True
            )
            embedVar.add_field(
                name="Synopsis",
                value=f"{seasonv1['anime'][0]['synopsis']}".replace(
                    "[Written by MAL Rewrite]", ""
                ),
                inline=True,
            )
            embedVar.add_field(
                name="Episodes",
                value=f"{seasonv1['anime'][0]['episodes']}",
                inline=True,
            )
            embedVar.add_field(
                name="Genre(s)",
                value=str([name["name"]
                          for name in seasonv1["anime"][0]["genres"]])
                .replace("'", "")
                .replace("[", "")
                .replace("]", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Theme(s)",
                value=str([name["name"]
                          for name in seasonv1["anime"][0]["themes"]])
                .replace("'", "")
                .replace("[", "")
                .replace("]", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Continuing",
                value=f"{seasonv1['anime'][0]['continuing']}",
                inline=True,
            )
            embedVar.add_field(
                name="Name", value=f"{seasonv1['anime'][1]['title']}", inline=True
            )
            embedVar.add_field(
                name="Synopsis",
                value=f"{seasonv1['anime'][1]['synopsis']}".replace(
                    "[Written by MAL Rewrite]", ""
                ),
                inline=True,
            )
            embedVar.add_field(
                name="Episodes",
                value=f"{seasonv1['anime'][1]['episodes']}",
                inline=True,
            )
            embedVar.add_field(
                name="Genre(s)",
                value=str([name["name"]
                          for name in seasonv1["anime"][1]["genres"]])
                .replace("'", "")
                .replace("[", "")
                .replace("]", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Theme(s)",
                value=str([name["name"]
                          for name in seasonv1["anime"][1]["themes"]])
                .replace("'", "")
                .replace("[", "")
                .replace("]", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Continuing",
                value=f"{seasonv1['anime'][1]['continuing']}",
                inline=True,
            )
            embedVar.add_field(
                name="Name", value=f"{seasonv1['anime'][2]['title']}", inline=True
            )
            embedVar.add_field(
                name="Synopsis",
                value=f"{seasonv1['anime'][2]['synopsis']}".replace(
                    "[Written by MAL Rewrite]", ""
                ),
                inline=True,
            )
            embedVar.add_field(
                name="Episodes",
                value=f"{seasonv1['anime'][2]['episodes']}",
                inline=True,
            )
            embedVar.add_field(
                name="Genre(s)",
                value=str([name["name"]
                          for name in seasonv1["anime"][2]["genres"]])
                .replace("'", "")
                .replace("[", "")
                .replace("]", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Theme(s)",
                value=str([name["name"]
                          for name in seasonv1["anime"][2]["themes"]])
                .replace("'", "")
                .replace("[", "")
                .replace("]", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Continuing",
                value=f"{seasonv1['anime'][2]['continuing']}",
                inline=True,
            )
            await ctx.send(embed=embedVar)
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
