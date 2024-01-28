import datetime
from typing import Dict, Optional
from urllib.parse import quote_plus

import ciso8601
import orjson
from aiohttp import ClientSession
from dateutil.parser import parse
from discord import PartialEmoji, app_commands
from discord.ext import commands
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from kumikocore import KumikoCore
from Libs.ui.search import (
    AniListAnime,
    AniListAnimePages,
    AniListManga,
    AniListMangaPages,
    AniListMediaTitle,
    ModrinthPages,
    ModrinthProject,
)
from Libs.utils.context import KContext
from Libs.utils.pages import EmbedListSource, KumikoPages
from typing_extensions import Annotated
from yarl import URL


class AIOHTTPTransportExistingSession(AIOHTTPTransport):
    def __init__(self, *args, client_session: ClientSession, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = client_session

    async def connect(self) -> None:
        pass

    async def close(self) -> None:
        pass


class ModrinthFlags(commands.FlagConverter):
    query: str = commands.flag(
        aliases=["q"], description="The Minecraft project to search for"
    )
    project_type: str = commands.flag(
        default="mod",
        description="The category to filter out. Can be mod, plugin, etc. Defaults to mod",
    )
    loader: str = commands.flag(
        default="fabric",
        description="The loader to filter out. Examples include fabric, forge, spigot, etc. Defaults to fabric",
    )
    version: str = commands.flag(
        default="1.16.5",
        description="The version to filter out. Examples include 1.16.5, etc. Defaults to 1.16.5",
    )


class Searches(commands.Cog):
    """Search for anime, manga, gifs, memes, and much more"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session
        self.tenor_key = self.bot.config["tenor"]
        self.api_url = "https://graphql.anilist.co/"

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<a:typing:597589448607399949>")

    def parse_anilist_dates(self, date: Dict[str, str]) -> Optional[datetime.datetime]:
        if None in date.values():
            return None
        formatted_date = f"{date['month']}-{date['day']}-{date['year']}"
        return parse(formatted_date)

    @commands.hybrid_command(name="lmgtfy")
    @app_commands.describe(query="What do you want to search?")
    async def lmgtfy(
        self, ctx: KContext, query: Annotated[str, commands.clean_content]
    ) -> None:
        """Let Me Google That For You"""
        url = URL("https://letmegooglethat.com") % {"q": quote_plus(query)}
        await ctx.send(str(url))

    @commands.hybrid_group(name="search")
    async def search(self, ctx: KContext) -> None:
        """Search for anime, manga, gifs, memes, and much more"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @search.command(name="anime")
    @app_commands.describe(name="The name of the anime to search")
    async def anime(self, ctx: KContext, *, name: str) -> None:
        """Searches up animes"""
        await ctx.defer()
        async with Client(
            transport=AIOHTTPTransportExistingSession(
                url=self.api_url, client_session=self.session
            ),
            fetch_schema_from_transport=True,
        ) as gql_session:
            query = gql(
                """
            query ($animeName: String!, $perPage: Int, $isAdult: Boolean!) {
                Page (perPage: $perPage){
                    media(search: $animeName, isAdult: $isAdult, type: ANIME) {
                        title {
                            native
                            english
                            romaji
                        }
                        status
                        description(asHtml: false)
                        format
                        status
                        startDate {
                            day
                            month
                            year
                        }
                        endDate {
                            day
                            month
                            year
                        }
                        episodes
                        duration
                        coverImage {
                            extraLarge
                            color
                        }
                        genres
                        tags {
                            name
                        }
                        source
                        synonyms
                        idMal
                        siteUrl
                        averageScore
                        meanScore
                        popularity
                        trending
                        isAdult

                    }
                }
            }
            """
            )

            params = {"animeName": name, "perPage": 25, "isAdult": False}
            data = await gql_session.execute(query, variable_values=params)

            if len(data["Page"]["media"]) == 0:
                await ctx.send("The anime was not found")
                return

            converted = [
                AniListAnime(
                    title=AniListMediaTitle(
                        native=anime["title"]["native"],
                        english=anime["title"]["english"],
                        romaji=anime["title"]["romaji"],
                    ),
                    status=anime["status"],
                    description=anime["description"],
                    format=anime["format"],
                    start_date=self.parse_anilist_dates(anime["startDate"]),
                    end_date=self.parse_anilist_dates(anime["endDate"]),
                    episodes=anime["episodes"],
                    duration=anime["duration"],
                    cover_image=anime["coverImage"]["extraLarge"],
                    cover_image_color=anime["coverImage"]["color"],
                    genres=anime["genres"],
                    tags=[tag["name"] for tag in anime["tags"]],
                    synonyms=anime["synonyms"],
                    mal_id=anime["idMal"],
                    site_url=anime["siteUrl"],
                    avg_score=anime["averageScore"],
                    mean_score=anime["meanScore"],
                    popularity=anime["popularity"],
                    trending=anime["trending"],
                    is_adult=anime["isAdult"],
                )
                for anime in data["Page"]["media"]
            ]
            pages = AniListAnimePages(converted, ctx=ctx)
            await pages.start()

    @search.command(name="manga")
    @app_commands.describe(name="The name of the manga to search")
    async def manga(self, ctx: KContext, *, name: str):
        """Searches for manga on AniList"""
        await ctx.defer()
        async with Client(
            transport=AIOHTTPTransportExistingSession(
                url=self.api_url, client_session=self.session
            ),
            fetch_schema_from_transport=True,
        ) as gql_session:
            query = gql(
                """
                query ($mangaName: String!, $perPage: Int, $isAdult: Boolean!) {
                    Page (perPage: $perPage){
                        media(search: $mangaName, isAdult: $isAdult, type: MANGA) {
                            title {
                                native
                                english
                                romaji
                            }
                            status
                            description(asHtml: false)
                            format
                            status
                            startDate {
                                day
                                month
                                year
                            }
                            endDate {
                                day
                                month
                                year
                            }
                            chapters
                            volumes
                            coverImage {
                                extraLarge
                                color
                            }
                            genres
                            tags {
                                name
                            }
                            source
                            synonyms
                            idMal
                            siteUrl
                            averageScore
                            meanScore
                            popularity
                            trending
                            isAdult

                        }
                    }
                }
                """
            )

            params = {"mangaName": name, "perPage": 25, "isAdult": False}
            data = await gql_session.execute(query, variable_values=params)
            if len(data["Page"]["media"]) == 0:
                await ctx.send("The manga(s) were not found")
                return

            converted = [
                AniListManga(
                    title=AniListMediaTitle(
                        native=manga["title"]["native"],
                        english=manga["title"]["english"],
                        romaji=manga["title"]["romaji"],
                    ),
                    status=manga["status"],
                    description=manga["description"],
                    format=manga["format"],
                    start_date=self.parse_anilist_dates(manga["startDate"]),
                    end_date=self.parse_anilist_dates(manga["endDate"]),
                    chapters=manga["chapters"],
                    volumes=manga["volumes"],
                    cover_image=manga["coverImage"]["extraLarge"],
                    cover_image_color=manga["coverImage"]["color"],
                    genres=manga["genres"],
                    tags=[tag["name"] for tag in manga["tags"]],
                    synonyms=manga["synonyms"],
                    mal_id=manga["idMal"],
                    site_url=manga["siteUrl"],
                    avg_score=manga["averageScore"],
                    mean_score=manga["meanScore"],
                    popularity=manga["popularity"],
                    trending=manga["trending"],
                    is_adult=manga["isAdult"],
                )
                for manga in data["Page"]["media"]
            ]
            pages = AniListMangaPages(converted, ctx=ctx)
            await pages.start()

    @search.command(name="gifs")
    @app_commands.describe(search="The search term to use")
    async def gifs(self, ctx: KContext, *, search: str) -> None:
        """Searches for gifs on Tenor"""
        url = URL("https://tenor.googleapis.com/v2/search")
        params = {
            "q": search,
            "key": self.tenor_key,
            "contentfilter": "medium",
            "limit": 25,
            "media_filter": "minimal",
        }
        async with self.session.get(url, params=params) as r:
            data = await r.json(loads=orjson.loads)
            if len(data["results"]) == 0 or r.status == 404:
                await ctx.send("The gifs were not found")
                return
            else:
                main_data = [
                    {"image": item["media_formats"]["gif"]["url"]}
                    for item in data["results"]
                ]
                embed_source = EmbedListSource(main_data, per_page=1)
                pages = KumikoPages(source=embed_source, ctx=ctx)
                await pages.start()

    @search.command(
        name="modrinth",
        usage="query: <str> project_type: <str> loader: <str> version: <str>",
    )
    async def modrinth(self, ctx: KContext, *, flags: ModrinthFlags) -> None:
        """Search for Minecraft projects on Modrinth"""
        url = URL("https://api.modrinth.com/v2/search")
        facets = [
            f"project_type:{flags.project_type.lower()}",
            f"categories:{flags.loader.lower()}",
            f"versions:{flags.version.lower()}",
        ]
        list_facets = [f'["{item}"]' for item in facets]
        params = {
            "query": flags.query,
            "limit": 25,
            "facets": f"[{','.join(list_facets).rstrip(',')}]",
        }
        async with self.session.get(url, params=params) as r:
            data = await r.json(loads=orjson.loads)
            if data["total_hits"] == 0:
                await ctx.send("The projects(s) were/was not found")
                return

            converted = [
                ModrinthProject(
                    title=item["title"],
                    description=item["description"],
                    display_categories=item["display_categories"],
                    client_side=item["client_side"],
                    server_side=item["server_side"],
                    project_type=item["project_type"],
                    project_slug=item["slug"],
                    downloads=item["downloads"],
                    icon_url=item["icon_url"],
                    author=item["author"],
                    versions=item["versions"],
                    latest_version=item["latest_version"],
                    date_created=ciso8601.parse_datetime(item["date_created"]),
                    date_updated=ciso8601.parse_datetime(item["date_modified"]),
                    license=item["license"],
                )
                for item in data["hits"]
            ]
            pages = ModrinthPages(converted, ctx=ctx)
            await pages.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Searches(bot))
