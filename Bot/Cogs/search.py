from urllib.parse import quote_plus

import ciso8601
import orjson
from discord import PartialEmoji, app_commands
from discord.ext import commands
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from kumikocore import KumikoCore
from Libs.cog_utils.search import ModrinthFlags
from Libs.ui.search import ModrinthPages, ModrinthProject
from Libs.utils.pages import EmbedListSource, KumikoPages
from typing_extensions import Annotated
from yarl import URL


class Searches(commands.Cog):
    """Search for anime, manga, gifs, memes, and much more"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session
        self._TENOR_KEY = self.bot.config["TENOR_API_KEY"]

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<a:typing:597589448607399949>")

    @commands.hybrid_command(name="lmgtfy")
    @app_commands.describe(query="What do you want to search?")
    async def lmgtfy(
        self, ctx: commands.Context, query: Annotated[str, commands.clean_content]
    ) -> None:
        """Let Me Google That For You"""
        query = quote_plus(query)
        url = URL("https://letmegooglethat.com") % {"q": query}
        await ctx.send(f"Link: {str(url)}")

    @commands.hybrid_group(name="search")
    async def search(self, ctx: commands.Context) -> None:
        """Search for anime, manga, gifs, memes, and much more"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @search.command(name="anime")
    @app_commands.describe(name="The name of the anime to search")
    async def anime(self, ctx: commands.Context, *, name: str) -> None:
        """Searches up animes"""
        async with Client(
            transport=AIOHTTPTransport(url="https://graphql.anilist.co/"),
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
                        description
                        format
                        status
                        seasonYear
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
                        coverImage {
                            extraLarge
                        }
                        genres
                        tags {
                            name
                        }
                        synonyms
                        id

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
            else:
                main_data = [
                    {
                        "title": item["title"]["romaji"],
                        "description": str(item["description"]).replace("<br>", ""),
                        "image": item["coverImage"]["extraLarge"],
                        "fields": [
                            {"name": "Native Name", "value": item["title"]["native"]},
                            {"name": "English Name", "value": item["title"]["english"]},
                            {"name": "Status", "value": item["status"]},
                            {
                                "name": "Start Date",
                                "value": f'{item["startDate"]["year"]}-{item["startDate"]["month"]}-{item["startDate"]["day"]}',
                            },
                            {
                                "name": "End Date",
                                "value": f'{item["endDate"]["year"]}-{item["endDate"]["month"]}-{item["endDate"]["day"]}',
                            },
                            {"name": "Genres", "value": item["genres"]},
                            {"name": "Synonyms", "value": item["synonyms"]},
                            {"name": "Format", "value": item["format"]},
                            {"name": "Season Year", "value": item["seasonYear"]},
                            {
                                "name": "Tags",
                                "value": [tagItem["name"] for tagItem in item["tags"]],
                            },
                            {
                                "name": "AniList URL",
                                "value": f"https://anilist.co/anime/{item['id']}",
                            },
                        ],
                    }
                    for item in data["Page"]["media"]
                ]
                embed_source = EmbedListSource(main_data, per_page=1)
                pages = KumikoPages(source=embed_source, ctx=ctx)
                await pages.start()

    @search.command(name="manga")
    @app_commands.describe(name="The name of the manga to search")
    async def manga(self, ctx: commands.Context, *, name: str):
        """Searches for manga on AniList"""
        async with Client(
            transport=AIOHTTPTransport(url="https://graphql.anilist.co/"),
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
                        description
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
                        coverImage {
                            extraLarge
                        }
                        genres
                        tags {
                            name
                        }
                        synonyms
                        id

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
            else:
                main_data = [
                    {
                        "title": item["title"]["romaji"],
                        "description": str(item["description"]).replace("<br>", ""),
                        "image": item["coverImage"]["extraLarge"],
                        "fields": [
                            {"name": "Native Name", "value": item["title"]["native"]},
                            {"name": "English Name", "value": item["title"]["english"]},
                            {"name": "Status", "value": item["status"]},
                            {
                                "name": "Start Date",
                                "value": f'{item["startDate"]["year"]}-{item["startDate"]["month"]}-{item["startDate"]["day"]}',
                            },
                            {
                                "name": "End Date",
                                "value": f'{item["endDate"]["year"]}-{item["endDate"]["month"]}-{item["endDate"]["day"]}',
                            },
                            {"name": "Genres", "value": item["genres"]},
                            {"name": "Synonyms", "value": item["synonyms"]},
                            {"name": "Format", "value": item["format"]},
                            {
                                "name": "Tags",
                                "value": [tagItem["name"] for tagItem in item["tags"]],
                            },
                            {
                                "name": "AniList URL",
                                "value": f"https://anilist.co/anime/{item['id']}",
                            },
                        ],
                    }
                    for item in data["Page"]["media"]
                ]
                embed_source = EmbedListSource(main_data, per_page=1)
                pages = KumikoPages(source=embed_source, ctx=ctx)
                await pages.start()

    @search.command(name="gifs")
    @app_commands.describe(search="The search term to use")
    async def gifs(self, ctx: commands.Context, *, search: str) -> None:
        """Searches for gifs on Tenor"""
        params = {
            "q": search,
            "key": self._TENOR_KEY,
            "contentfilter": "medium",
            "limit": 25,
            "media_filter": "minimal",
        }
        async with self.session.get(
            "https://tenor.googleapis.com/v2/search", params=params
        ) as r:
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
    async def modrinth(self, ctx: commands.Context, *, flags: ModrinthFlags) -> None:
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
