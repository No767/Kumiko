import os
from datetime import datetime
from typing import Literal, Optional

import aiohttp
import asyncpraw
import orjson
from discord.ext import commands
from discord.utils import format_dt
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from Libs.utils import parseSubreddit
from Libs.utils.pages import EmbedListSource, KumikoPages

load_dotenv()

GITHUB_API_KEY = os.environ["GITHUB_API_KEY"]
REDDIT_ID = os.environ["REDDIT_ID"]
REDDIT_SECRET = os.environ["REDDIT_SECRET"]
TENOR_API_KEY = os.environ["TENOR_API_KEY"]


class Searches(commands.Cog):
    """Search for anime, manga, gifs, memes, and much more!"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_group(name="search")
    async def search(self, ctx: commands.Context) -> None:
        """Base parent command for searches - See the subcommands for more info"""
        ...

    @search.command(name="anime")
    async def searchAnime(self, ctx: commands.Context, *, name: str) -> None:
        """Searches up animes

        Args:
            ctx (commands.Context): Base context
            name (str): The name of the anime to look up
        """
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
    async def searchManga(self, ctx: commands.Context, *, name: str):
        """Searches for manga on AniList

        Args:
            ctx (commands.Context): Base context
            name (str): The name of the manga to look up
        """
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
    async def searchGifs(self, ctx: commands.Context, *, search: str) -> None:
        """Searches for gifs on Tenor

        Args:
            ctx (commands.Context): Base context
            search (str): The search term to use
        """
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

    @search.command(name="memes")
    async def searchMemes(
        self, ctx: commands.Context, subreddit: str, amount: Optional[int] = 5
    ) -> None:
        """Searches for memes on Reddit

        Args:
            ctx (commands.Context): Base context
            subreddit (str): The subreddit to search
            amount (Optional[int], optional): The amount of memes to return. Defaults to 5.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://meme-api.com/gimme/{parseSubreddit(subreddit)}/{amount}"
            ) as r:
                data = await r.json(loads=orjson.loads)
                mainData = [
                    {
                        "title": item["title"],
                        "image": item["url"],
                        "fields": [
                            {"name": "Author", "value": item["author"]},
                            {"name": "Subreddit", "value": item["subreddit"]},
                            {"name": "Upvotes", "value": item["ups"]},
                            {"name": "NSFW", "value": item["nsfw"]},
                            {"name": "Spoiler", "value": item["spoiler"]},
                            {"name": "Reddit URL", "value": item["postLink"]},
                        ],
                    }
                    for item in data["memes"]
                ]
                embedSource = EmbedListSource(mainData, per_page=1)
                pages = KumikoPages(source=embedSource, ctx=ctx)
                await pages.start()

    @search.command(name="reddit-feed")
    async def redditFeed(
        self,
        ctx: commands.Context,
        subreddit: str,
        filter: Optional[Literal["New", "Hot", "Rising"]] = "New",
    ) -> None:
        """Gets a feed of posts from a subreddit

        Args:
            ctx (commands.Context): Base context
            subreddit (str): Subreddit to search
            filter (Optional[Literal["New", "Hot", "Rising"]], optional): Sort filters. Defaults to "New".
        """
        async with asyncpraw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="Kumiko (by /u/No767)",
        ) as reddit:
            sub = await reddit.subreddit(parseSubreddit(subreddit))
            subGen = (
                sub.new(limit=25)
                if filter == "New"
                else sub.hot(limit=25)
                if filter == "Hot"
                else sub.rising(limit=25)
            )
            data = [
                {
                    "title": post.title,
                    "description": post.selftext,
                    "image": post.url,
                    "fields": [
                        {"name": "Author", "value": post.author},
                        {"name": "Upvotes", "value": post.score},
                        {"name": "NSFW", "value": post.over_18},
                        {"name": "Flair", "value": post.link_flair_text},
                        {"name": "Number of Comments", "value": post.num_comments},
                        {
                            "name": "Reddit URL",
                            "value": f"https://reddit.com{post.permalink}",
                        },
                        {
                            "name": "Created At",
                            "value": format_dt(
                                datetime.fromtimestamp(post.created_utc)
                            ),
                        },
                    ],
                }
                async for post in subGen
            ]
            embedSource = EmbedListSource(data, per_page=1)
            pages = KumikoPages(source=embedSource, ctx=ctx)
            await pages.start()

    @search.command(name="reddit-eggirl")
    async def redditEggIRL(
        self,
        ctx: commands.Context,
        filter: Optional[Literal["New", "Hot", "Rising"]] = "New",
    ) -> None:
        """Literally just shows you r/egg_irl posts. No comment.

        Args:
            ctx (commands.Context): Base context
            filter (Optional[Literal["New", "Hot", "Rising"]], optional): Sort filters. Defaults to "New".
        """
        async with asyncpraw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="Kumiko (by /u/No767)",
        ) as reddit:
            sub = await reddit.subreddit(parseSubreddit("egg_irl"))
            subGen = (
                sub.new(limit=25)
                if filter == "New"
                else sub.hot(limit=25)
                if filter == "Hot"
                else sub.rising(limit=25)
            )
            data = [
                {
                    "title": post.title,
                    "description": post.selftext,
                    "image": post.url,
                    "fields": [
                        {"name": "Author", "value": post.author},
                        {"name": "Upvotes", "value": post.score},
                        {"name": "NSFW", "value": post.over_18},
                        {"name": "Flair", "value": post.link_flair_text},
                        {"name": "Number of Comments", "value": post.num_comments},
                        {
                            "name": "Reddit URL",
                            "value": f"https://reddit.com{post.permalink}",
                        },
                        {
                            "name": "Created At",
                            "value": format_dt(
                                datetime.fromtimestamp(post.created_utc)
                            ),
                        },
                    ],
                }
                async for post in subGen
            ]
            embedSource = EmbedListSource(data, per_page=1)
            pages = KumikoPages(source=embedSource, ctx=ctx)
            await pages.start()

    @search.command(name="reddit")
    async def redditSearch(
        self, ctx: commands.Context, *, search: str, subreddit: Optional[str] = "all"
    ) -> None:
        """Searches for base context

        Args:
            ctx (commands.Context): Base context
            search (str): The search query to use
            subreddit (Optional[str], optional): Which subreddit to use. Defaults to "all".
        """
        async with asyncpraw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="Kumiko (by /u/No767)",
        ) as reddit:
            sub = await reddit.subreddit(parseSubreddit(subreddit))
            data = [
                {
                    "title": post.title,
                    "description": post.selftext,
                    "image": post.url,
                    "fields": [
                        {"name": "Author", "value": post.author},
                        {"name": "Upvotes", "value": post.score},
                        {"name": "NSFW", "value": post.over_18},
                        {"name": "Flair", "value": post.link_flair_text},
                        {"name": "Number of Comments", "value": post.num_comments},
                        {
                            "name": "Reddit URL",
                            "value": f"https://reddit.com{post.permalink}",
                        },
                        {
                            "name": "Created At",
                            "value": format_dt(
                                datetime.fromtimestamp(post.created_utc)
                            ),
                        },
                    ],
                }
                async for post in sub.search(search)
            ]
            embedSource = EmbedListSource(data, per_page=1)
            pages = KumikoPages(source=embedSource, ctx=ctx)
            await pages.start()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Searches(bot))
