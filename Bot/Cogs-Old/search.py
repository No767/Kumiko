import os
import random
from datetime import datetime

import aiohttp
import asyncpraw
import ciso8601
import discord
import orjson
import simdjson
from asyncprawcore.exceptions import NotFound
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from discord.utils import format_dt
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from rin_exceptions import HTTPException, NoItemsError

load_dotenv()

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
REDDIT_ID = os.getenv("REDDIT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
TENOR_API_KEY = os.getenv("TENOR_API_KEY")

parser = simdjson.Parser()


class Search(commands.Cog):
    """Search for anime, manga, gifs, memes, and much more!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    search = SlashCommandGroup("search")
    searchGithub = search.create_subgroup(
        "github", "Search for repos and releases on GitHub"
    )
    searchReddit = search.create_subgroup("reddit", "Search memes and posts on Reddit")

    @search.command(name="anime")
    async def aniListSearchAnime(
        self,
        ctx: discord.ApplicationContext,
        name: Option(str, "The name of the anime"),
    ) -> None:
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
            try:
                if len(data["Page"]["media"]) == 0:
                    raise NoItemsError
                else:
                    mainPages = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=mainItem["title"]["romaji"],
                                description=str(mainItem["description"]).replace(
                                    "<br>", ""
                                ),
                            )
                            .add_field(
                                name="Native Name",
                                value=f'[{mainItem["title"]["native"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="English Name",
                                value=f'[{mainItem["title"]["english"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="Status", value=mainItem["status"], inline=True
                            )
                            .add_field(
                                name="Start Date",
                                value=f'{mainItem["startDate"]["year"]}-{mainItem["startDate"]["month"]}-{mainItem["startDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="End Date",
                                value=f'{mainItem["endDate"]["year"]}-{mainItem["endDate"]["month"]}-{mainItem["endDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="Genres", value=mainItem["genres"], inline=True
                            )
                            .add_field(
                                name="Synonyms", value=mainItem["synonyms"], inline=True
                            )
                            .add_field(
                                name="Format", value=mainItem["format"], inline=True
                            )
                            .add_field(
                                name="Season Year",
                                value=mainItem["seasonYear"],
                                inline=True,
                            )
                            .add_field(
                                name="Tags",
                                value=[tagItem["name"] for tagItem in mainItem["tags"]],
                                inline=True,
                            )
                            .add_field(
                                name="AniList URL",
                                value=f"https://anilist.co/anime/{mainItem['id']}",
                                inline=True,
                            )
                            .set_image(url=mainItem["coverImage"]["extraLarge"])
                            for mainItem in data["Page"]["media"]
                        ],
                        loop_pages=True,
                    )
                    await mainPages.respond(ctx.interaction, ephemeral=False)
            except NoItemsError:
                embedNoItemsError = discord.Embed()
                embedNoItemsError.description = "Sorry, but there seems to be no anime(s) with that name. Please try again"
                await ctx.respond(embed=embedNoItemsError)

    @search.command(name="manga")
    async def aniListSearchManga(
        self,
        ctx: discord.ApplicationContext,
        name: Option(str, "The name of the manga"),
    ) -> None:
        """Searches for up to 25 mangas on AniList"""
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
            try:
                if len(data["Page"]["media"]) == 0:
                    raise NoItemsError
                else:
                    mainPages2 = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=mainItem["title"]["romaji"],
                                description=str(mainItem["description"]).replace(
                                    "<br>", ""
                                ),
                            )
                            .add_field(
                                name="Native Name",
                                value=f'[{mainItem["title"]["native"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="English Name",
                                value=f'[{mainItem["title"]["english"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="Status", value=mainItem["status"], inline=True
                            )
                            .add_field(
                                name="Start Date",
                                value=f'{mainItem["startDate"]["year"]}-{mainItem["startDate"]["month"]}-{mainItem["startDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="End Date",
                                value=f'{mainItem["endDate"]["year"]}-{mainItem["endDate"]["month"]}-{mainItem["endDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="Genres", value=mainItem["genres"], inline=True
                            )
                            .add_field(
                                name="Synonyms", value=mainItem["synonyms"], inline=True
                            )
                            .add_field(
                                name="Format", value=mainItem["format"], inline=True
                            )
                            .add_field(
                                name="Tags",
                                value=[tagItem["name"] for tagItem in mainItem["tags"]],
                                inline=True,
                            )
                            .add_field(
                                name="AniList URL",
                                value=f"https://anilist.co/manga/{mainItem['id']}",
                                inline=True,
                            )
                            .set_image(url=mainItem["coverImage"]["extraLarge"])
                            for mainItem in data["Page"]["media"]
                        ],
                        loop_pages=True,
                    )

                    await mainPages2.respond(ctx.interaction, ephemeral=False)
            except NoItemsError:
                embedNoItemsError = discord.Embed()
                embedNoItemsError.description = "Sorry, but there seems to be no manga(s) with that name. Please try again"
                await ctx.respond(embed=embedNoItemsError)

    @search.command(name="gifs")
    async def searchTenor(
        self,
        ctx: discord.ApplicationContext,
        search: Option(str, "The text to be searched"),
        amount: Option(
            int, "The amount of gifs to search for", default=1, min=1, max=25
        ),
    ) -> None:
        """Searches for gifs on tenor"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": search,
                "key": TENOR_API_KEY,
                "contentfilter": "medium",
                "limit": amount,
                "media_filter": "minimal",
            }
            async with session.get(
                "https://tenor.googleapis.com/v2/search", params=params
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if len(dataMain["results"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=dictItem["content_description"]
                                ).set_image(url=dictItem["media_formats"]["gif"]["url"])
                                for dictItem in dataMain["results"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedNoItemsError = discord.Embed()
                    embedNoItemsError.description = "No GIFs found for that search term"
                    await ctx.respond(embed=embedNoItemsError)

    @searchReddit.command(name="memes")
    async def searchRedditMemes(
        self,
        ctx: discord.ApplicationContext,
        subreddit: Option(str, "The subreddit to search memes in", required=False),
        amount: Option(
            int,
            "How much memes do you want returned?",
            default=25,
            min_value=1,
            max_value=50,
        ),
    ) -> None:
        """Searches for memes on reddit"""
        if subreddit is None:
            listOfSubs = [
                "memes",
                "dankmemes",
                "me_irl",
            ]
            sub = random.choice(listOfSubs)  # nosec
        elif "r/" in subreddit:
            subSplit = sub.split("/")
            sub = subSplit[1]
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://meme-api.herokuapp.com/gimme/{sub}/{amount}"
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if len(dataMain["memes"]) == 0 or r.status == 404:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(title=items["title"])
                                .add_field(
                                    name="Author", value=items["author"], inline=True
                                )
                                .add_field(
                                    name="Subreddit",
                                    value=items["subreddit"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Upvotes", value=items["ups"], inline=True
                                )
                                .add_field(
                                    name="NSFW", value=items["nsfw"], inline=True
                                )
                                .add_field(
                                    name="Spoiler", value=items["spoiler"], inline=True
                                )
                                .add_field(
                                    name="Reddit URL",
                                    value=items["postLink"],
                                    inline=True,
                                )
                                .set_image(url=items["url"])
                                for items in dataMain["memes"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = "Sorry, but there are no memes to be found within that subreddit. Please try again."
                    await ctx.respond(embedError)

    @searchReddit.command(name="feed")
    async def redditFeed(
        self,
        ctx: discord.ApplicationContext,
        *,
        subreddit: Option(
            str, "The subreddit to look for (Dont't include r/ within the subreddit)"
        ),
        filters: Option(str, "New, Hot, or Rising", choices=["New", "Hot", "Rising"]),
    ) -> None:
        """Returns up to 25 reddit posts based on the current filter"""
        async with asyncpraw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="kumiko (by /u/No767)",
        ) as redditapi:
            try:
                try:
                    sub = subreddit
                    if "r/" in subreddit:
                        subSplit = sub.split("/")
                        sub = subSplit[1]
                    mainSub = await redditapi.subreddit(str(sub))
                    if "New" in filters:
                        subLooper = mainSub.new(limit=25)
                    elif "Hot" in filters:
                        subLooper = mainSub.hot(limit=25)
                    elif "Rising" in filters:
                        subLooper = mainSub.rising(limit=25)
                    idealPages2 = [
                        discord.Embed(
                            title=submission.title, description=submission.selftext
                        )
                        .add_field(
                            name="Author", value=submission.author.name, inline=True
                        )
                        .add_field(
                            name="URL",
                            value=f"https://reddit.com{submission.permalink}",
                            inline=True,
                        )
                        .add_field(name="Upvotes", value=submission.score, inline=True)
                        .add_field(name="NSFW?", value=submission.over_18, inline=True)
                        .add_field(
                            name="Flair",
                            value=submission.link_flair_text,
                            inline=True,
                        )
                        .add_field(
                            name="Number of comments",
                            value=submission.num_comments,
                            inline=True,
                        )
                        .add_field(
                            name="Created At (UTC, 24hr)",
                            value=format_dt(
                                datetime.datetime.fromtimestamp(submission.created_utc)
                            ),
                            inline=True,
                        )
                        .set_image(url=submission.url)
                        async for submission in subLooper
                    ]
                    mainPages = pages.Paginator(pages=idealPages2, loop_pages=True)
                    await mainPages.respond(ctx.interaction, ephemeral=False)
                except NotFound:
                    notFound = discord.Embed()
                    notFound.description = (
                        "Sorry, but that subreddit can't be found. Please try again."
                    )
                    await ctx.respond(embed=notFound)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again..."
                embedError.add_field(
                    name="Error Message",
                    value=f"{e.__module__}.{e.__class__.__name__}: {str(e)}",
                    inline=True,
                )
                await ctx.respond(embed=embedError)

    @searchReddit.command(name="egg_irl")
    async def redditEgg(
        self,
        ctx: discord.ApplicationContext,
        filters: Option(str, "New, Top or Hot", choices=["New", "Top", "Rising"]),
    ) -> None:
        """Literally just shows you r/egg_irl posts. No comment."""
        async with asyncpraw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="kumiko (by /u/No767)",
        ) as redditapi:
            try:
                mainSub = await redditapi.subreddit("egg_irl")

                if "New" in filters:
                    subLooper = mainSub.new(limit=25)
                elif "Top" in filters:
                    subLooper = mainSub.top(limit=25)
                elif "Rising" in filters:
                    subLooper = mainSub.rising(limit=25)
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=submission.title, description=submission.selftext
                        )
                        .add_field(name="Author", value=submission.author, inline=True)
                        .add_field(
                            name="URL",
                            value=f"https://reddit.com{submission.permalink}",
                            inline=True,
                        )
                        .add_field(name="Upvotes", value=submission.score, inline=True)
                        .add_field(name="NSFW?", value=submission.over_18, inline=True)
                        .add_field(
                            name="Flair", value=submission.link_flair_text, inline=True
                        )
                        .add_field(
                            name="Number of comments",
                            value=submission.num_comments,
                            inline=True,
                        )
                        .add_field(
                            name="Created At (UTC, 24hr)",
                            value=format_dt(
                                datetime.datetime.fromtimestamp(submission.created_utc)
                            ),
                            inline=True,
                        )
                        .set_image(url=submission.url)
                        async for submission in subLooper
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again..."
                embedError.add_field(
                    name="Error Message",
                    value=f"{e.__module__}.{e.__class__.__name__}: {str(e)}",
                    inline=True,
                )
                await ctx.respond(embed=embedError)

    @search.command(name="mc-mods")
    async def modrinthSearch(
        self,
        ctx: discord.ApplicationContext,
        *,
        mod: Option(str, "The name of the mod"),
        modloader: Option(
            str, "Forge or Fabric", choices=["Forge", "Fabric"], default="Forge"
        ),
    ) -> None:
        """Searches for Minecraft mods and plugins"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "query": mod,
                "index": "relevance",
                "limit": 25,
                "facets": f'[["categories:{str(modloader).lower()}"]]',
            }
            async with session.get(
                "https://api.modrinth.com/v2/search", params=params
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if len(dataMain["hits"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=mainItem["title"],
                                    description=mainItem["description"],
                                )
                                .add_field(
                                    name="Author", value=mainItem["author"], inline=True
                                )
                                .add_field(
                                    name="Categories",
                                    value=mainItem["categories"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Versions",
                                    value=mainItem["versions"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Latest Version",
                                    value=mainItem["latest_version"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Date Created",
                                    value=format_dt(
                                        ciso8601.parse_datetime(
                                            mainItem["date_created"]
                                        )
                                    ),
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Updated",
                                    value=format_dt(
                                        ciso8601.parse_datetime(
                                            mainItem["date_modified"]
                                        )
                                    ),
                                    inline=True,
                                )
                                .add_field(
                                    name="Downloads",
                                    value=mainItem["downloads"],
                                    inline=True,
                                )
                                .add_field(
                                    name="License",
                                    value=mainItem["license"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Mod URL",
                                    value=f"https://modrinth.com/mod/{mainItem['slug']}",
                                    inline=True,
                                )
                                .set_thumbnail(url=mainItem["icon_url"])
                                for mainItem in dataMain["hits"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = (
                        f"Sorry, but there are no mods named {mod}. Please try again"
                    )
                    await ctx.respond(embed=embedErrorMain)

    @searchGithub.command(name="release-list")
    async def githubReleasesList(
        self,
        ctx: discord.ApplicationContext,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
    ) -> None:
        """Lists out up to 25 releases of any repo"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {GITHUB_API_KEY}",
                "accept": "application/vnd.github.v3+json",
            }
            params = {"per_page": 25}
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/releases",
                headers=headers,
                params=params,
            ) as r:
                try:

                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    try:
                        if r.status == 404:
                            raise HTTPException
                        elif len(dataMain) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        title=dictItem5["name"],
                                        description=dictItem5["body"],
                                    )
                                    .add_field(
                                        name="URL",
                                        value=dictItem5["html_url"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Created At",
                                        value=ciso8601.parse_datetime(
                                            dictItem5["created_at"]
                                        ),
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Published At",
                                        value=format_dt(
                                            ciso8601.parse_datetime(
                                                dictItem5["published_at"]
                                            )
                                        ),
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Tarball URL",
                                        value=dictItem5["tarball_url"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Zipball URL",
                                        value=dictItem5["zipball_url"],
                                    )
                                    .add_field(
                                        name="Author",
                                        value=dictItem5["author"]["login"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Download URL",
                                        value=str(
                                            [
                                                items5["browser_download_url"]
                                                for items5 in dictItem5["assets"]
                                            ]
                                        ).replace("'", ""),
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Download Count",
                                        value=str(
                                            [
                                                items6["download_count"]
                                                for items6 in dictItem5["assets"]
                                            ]
                                        ).replace("'", ""),
                                        inline=True,
                                    )
                                    .set_thumbnail(
                                        url=dictItem5["author"]["avatar_url"]
                                    )
                                    for dictItem5 in dataMain
                                ],
                                loop_pages=True,
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        await ctx.respond(
                            embed=discord.Embed(
                                description="It seems like that there isn't a release for that repo. Please try again"
                            )
                        )
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, there seems to be no releases in that repo. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    @searchGithub.command(name="release-latest")
    async def githubLatestRelease(
        self,
        ctx: discord.ApplicationContext,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The repo's name"),
    ) -> None:
        """Gets the latest published full release for any repo"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {GITHUB_API_KEY}",
                "accept": "application/vnd.github.v3+json",
            }
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}/releases/latest",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    if r.status == 404:
                        raise HTTPException
                    else:
                        pageGroupsList = [
                            pages.PageGroup(
                                pages=[
                                    discord.Embed(
                                        title=dataMain["name"],
                                        description=dataMain["body"],
                                    )
                                    .add_field(name="URL", value=dataMain["html_url"])
                                    .add_field(
                                        name="Pre-release?",
                                        value=dataMain["prerelease"],
                                    )
                                    .add_field(name="Tag", value=dataMain["tag_name"])
                                    .add_field(
                                        name="Author", value=dataMain["author"]["login"]
                                    )
                                    .add_field(
                                        name="Created At",
                                        value=format_dt(
                                            ciso8601.parse_datetime(
                                                dataMain["created_at"]
                                            )
                                        ),
                                    )
                                    .add_field(
                                        name="Updated At",
                                        value=format_dt(
                                            ciso8601.parse_datetime(
                                                dataMain["published_at"]
                                            )
                                        )
                                        if dataMain["published_at"] is not None
                                        else "None",
                                    )
                                ],
                                label="Release Information",
                                description="Page for release information",
                            ),
                            pages.PageGroup(
                                pages=[
                                    discord.Embed(
                                        title=item["name"], description=item["label"]
                                    )
                                    .add_field(
                                        name="URL", value=item["browser_download_url"]
                                    )
                                    .add_field(
                                        name="Uploader", value=item["uploader"]["login"]
                                    )
                                    .add_field(name="Size", value=item["size"])
                                    .add_field(
                                        name="Content Type", value=item["content_type"]
                                    )
                                    .add_field(
                                        name="Download Count",
                                        value=item["download_count"],
                                    )
                                    .add_field(
                                        name="Created At",
                                        value=format_dt(
                                            ciso8601.parse_datetime(item["created_at"])
                                        ),
                                    )
                                    for item in dataMain["assets"]
                                ],
                                label="Assets",
                                description="Page for downloadable assets and information",
                            ),
                        ]
                        mainPages = pages.Paginator(
                            pages=pageGroupsList, show_menu=True, loop_pages=True
                        )
                        await mainPages.respond(ctx.interaction)
                except HTTPException:
                    embedHTTPExceptionError = discord.Embed()
                    embedHTTPExceptionError.description = "Sorry, but it seems like either there was no release or the repo doesn't exist. Please try again"
                    await ctx.respond(embed=embedHTTPExceptionError)

    @searchGithub.command(name="repo")
    async def searchGithubRepo(
        self,
        ctx: discord.ApplicationContext,
        owner: Option(str, "The owner of the repo"),
        repo: Option(str, "The name of the repo"),
    ) -> None:
        """Searches for one repo on GitHub"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"token {GITHUB_API_KEY}",
                "accept": "application/vnd.github.v3+json",
            }
            async with session.get(
                f"https://api.github.com/repos/{owner}/{repo}", headers=headers
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embed = discord.Embed()
                embed.title = dataMain["name"]
                embed.description = dataMain["description"]
                embed.set_thumbnail(url=dataMain["owner"]["avatar_url"])
                embed.add_field(name="Fork", value=dataMain["fork"])
                embed.add_field(name="Private", value=dataMain["private"])
                embed.add_field(name="Stars", value=dataMain["stargazers_count"])
                embed.add_field(
                    name="Language",
                    value=dataMain["language"]
                    if dataMain["language"] is not None
                    else "None",
                )
                embed.add_field(name="URL", value=dataMain["html_url"])
                embed.add_field(
                    name="Homepage",
                    value=dataMain["homepage"]
                    if dataMain["homepage"] is not None
                    else "None",
                )
                embed.add_field(
                    name="Created At",
                    value=format_dt(ciso8601.parse_datetime(dataMain["created_at"])),
                    inline=True,
                )
                embed.add_field(
                    name="Updated At",
                    value=format_dt(ciso8601.parse_datetime(dataMain["updated_at"])),
                    inline=True,
                )
                embed.add_field(
                    name="Pushed At",
                    value=format_dt(ciso8601.parse_datetime(dataMain["pushed_at"])),
                    inline=True,
                )
                await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Search(bot))
