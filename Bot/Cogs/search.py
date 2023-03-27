import os
from typing import Literal, Optional

import aiohttp
import ciso8601
import orjson
from discord import app_commands
from discord.ext import commands
from discord.utils import format_dt
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from Libs.utils.pages import EmbedListSource, KumikoPages

load_dotenv()

TENOR_API_KEY = os.environ["TENOR_API_KEY"]


class Searches(commands.Cog):
    """Search for anime, manga, gifs, memes, and much more!"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_group(name="search")
    async def search(self, ctx: commands.Context) -> None:
        """Base parent command for searches - See the subcommands for more info"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @search.command(name="anime")
    @app_commands.describe(name="The name of the anime to search")
    async def searchAnime(self, ctx: commands.Context, *, name: str) -> None:
        """Searches up animes"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
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
            data = await session.execute(query, variable_values=params)

            mainData = [
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
            embedSource = EmbedListSource(mainData, per_page=1)
            pages = KumikoPages(source=embedSource, ctx=ctx)
            await pages.start()

    @search.command(name="manga")
    @app_commands.describe(name="The name of the manga to search")
    async def searchManga(self, ctx: commands.Context, *, name: str):
        """Searches for manga on AniList"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
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
            data = await session.execute(query, variable_values=params)
            mainData = [
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
            embedSource = EmbedListSource(mainData, per_page=1)
            pages = KumikoPages(source=embedSource, ctx=ctx)
            await pages.start()

    @search.command(name="gifs")
    @app_commands.describe(search="The search term to use")
    async def searchGifs(self, ctx: commands.Context, *, search: str) -> None:
        """Searches for gifs on Tenor"""
        async with aiohttp.ClientSession() as session:
            params = {
                "q": search,
                "key": TENOR_API_KEY,
                "contentfilter": "medium",
                "limit": 25,
                "media_filter": "minimal",
            }
            async with session.get(
                "https://tenor.googleapis.com/v2/search", params=params
            ) as r:
                data = await r.json(loads=orjson.loads)
                mainData = [
                    {"image": item["media_formats"]["gif"]["url"]}
                    for item in data["results"]
                ]
                embedSource = EmbedListSource(mainData, per_page=1)
                pages = KumikoPages(source=embedSource, ctx=ctx)
                await pages.start()

    @search.command(name="mc-mods")
    @app_commands.describe(
        mod_name="The name of the mod to search for",
        modloader="Which modloader to use. Defaults to Forge.",
    )
    async def searchMods(
        self,
        ctx: commands.Context,
        *,
        mod_name: str,
        modloader: Optional[Literal["Forge", "Fabric"]] = "Forge",
    ) -> None:
        """Search for Minecraft mods and plugins on Modrinth"""
        async with aiohttp.ClientSession() as session:
            params = {
                "query": mod_name,
                "index": "relevance",
                "limit": 25,
                "facets": f'[["categories:{str(modloader).lower()}"]]',
            }
            async with session.get(
                "https://api.modrinth.com/v2/search", params=params
            ) as r:
                data = await r.json(loads=orjson.loads)
                mainData = [
                    {
                        "title": item["title"],
                        "description": item["description"],
                        "thumbnail": item["icon_url"],
                        "fields": [
                            {"name": "Author", "value": item["author"]},
                            {"name": "Categories", "value": item["categories"]},
                            {"name": "Versions", "value": item["versions"]},
                            {"name": "Latest Version", "value": item["latest_version"]},
                            {
                                "name": "Date Created",
                                "value": format_dt(
                                    ciso8601.parse_datetime(item["date_created"])
                                ),
                            },
                            {
                                "name": "Date Modified",
                                "value": format_dt(
                                    ciso8601.parse_datetime(item["date_modified"])
                                ),
                            },
                            {"name": "Downloads", "value": item["downloads"]},
                            {"name": "License", "value": item["license"]},
                            {
                                "name": "Modrinth URL",
                                "value": f"https://modrinth.com/{item['project_type']}/{item['slug']}",
                            },
                        ],
                    }
                    for item in data["hits"]
                ]
                embedSource = EmbedListSource(mainData, per_page=1)
                pages = KumikoPages(source=embedSource, ctx=ctx)
                await pages.start()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Searches(bot))
