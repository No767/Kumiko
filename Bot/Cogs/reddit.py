import asyncio
import datetime
import os

import aiohttp
import asyncpraw
import discord
import numpy as np
import orjson
import simdjson
import uvloop
from asyncprawcore.exceptions import NotFound
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from numpy.random import default_rng
from rin_exceptions import NoItemsError

load_dotenv()

Reddit_ID = os.getenv("Reddit_ID")
Reddit_Secret = os.getenv("Reddit_Secret")
jsonParser = simdjson.Parser()


class RedditV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    reddit = SlashCommandGroup("reddit", "Commands for Reddit Service")
    redditUsers = reddit.create_subgroup("users", "Subgroup for Reddit Users")

    @reddit.command(name="search")
    async def redditSearch(
        self,
        ctx,
        *,
        search: Option(
            str,
            "The query you want to search. Also supports searching subreddits as well",
        ),
    ):
        """Searches on Reddit for Content"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="alpine:rin:v2.2.4 (by /u/No767)",
        ) as api:
            sub = "all"
            try:
                if "r/" in search:
                    search = search.split("/")
                    sub = search[1]
                    search = "all"
                sub = await api.subreddit(sub)
                searcher = sub.search(query=search)
                posts = np.array(
                    [
                        post
                        async for post in searcher
                        if ".jpg" in post.url
                        or ".png" in post.url
                        or ".gif" in post.url
                        and not post.over_18
                    ]
                )
                rng = default_rng()
                try:
                    if len(posts) == 0:
                        raise NoItemsError
                    else:
                        post = rng.choice(a=posts, replace=False)
                        submission = post
                        await post.author.load()
                        reddit_embed = discord.Embed(
                            color=discord.Color.from_rgb(255, 69, 0)
                        )
                        reddit_embed.title = submission.title
                        reddit_embed.description = submission.selftext
                        reddit_embed.set_image(url=submission.url)
                        reddit_embed.add_field(
                            name="Author", value=submission.author.name, inline=True
                        )
                        reddit_embed.add_field(
                            name="Subreddit",
                            value=f"r/{submission.subreddit.display_name}",
                            inline=True,
                        )
                        reddit_embed.add_field(
                            name="URL",
                            value=f"https://reddit.com{submission.permalink}",
                            inline=True,
                        )
                        reddit_embed.add_field(
                            name="Upvotes", value=submission.score, inline=True
                        )
                        reddit_embed.add_field(
                            name="NSFW?", value=submission.over_18, inline=True
                        )
                        reddit_embed.add_field(
                            name="Flair", value=submission.link_flair_text, inline=True
                        )
                        reddit_embed.add_field(
                            name="Number of comments",
                            value=submission.num_comments,
                            inline=True,
                        )
                        reddit_embed.add_field(
                            name="Created At (UTC, 24hr)",
                            value=datetime.datetime.fromtimestamp(
                                submission.created_utc
                            ).strftime("%Y-%m-%d %H:%M"),
                            inline=True,
                        )
                        reddit_embed.add_field(
                            name="Created At (UTC, 12hr or AM/PM)",
                            value=datetime.datetime.fromtimestamp(
                                submission.created_utc
                            ).strftime("%Y-%m-%d %I:%M %p"),
                            inline=True,
                        )
                        await ctx.respond(embed=reddit_embed)
                except NoItemsError:
                    await ctx.respond(
                        embed=discord.Embed(
                            description=f"It seems like there are no posts that could be found with the query {search}. Please try again"
                        )
                    )
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again..."
                embedError.add_field(
                    name="Error Message",
                    value=f"{e.__module__}.{e.__class__.__name__}: {str(e)}",
                    inline=True,
                )
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="memes")
    async def redditMemes(
        self,
        ctx,
        *,
        subreddit: Option(str, "The subreddit to search memes in", required=False),
        amount: Option(
            int,
            "How much memes do you want returned?",
            default=25,
            min_value=1,
            max_value=50,
        ),
    ):
        """Gets some memes from Reddit"""
        sub = subreddit
        if subreddit is None:
            listOfSubs = np.array(
                [
                    "memes",
                    "dankmemes",
                    "me_irl",
                ]
            )
            rng = default_rng()
            sub = rng.choice(a=listOfSubs, replace=False)
        elif "r/" in subreddit:
            subSplit = sub.split("/")
            sub = subSplit[1]
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://meme-api.herokuapp.com/gimme/{sub}/{amount}"
            ) as r:
                data = await r.content.read()
                dataMain = jsonParser.parse(data, recursive=True)
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

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="feed")
    async def redditFeed(
        self,
        ctx,
        *,
        subreddit: Option(
            str, "The subreddit to look for (Dont't include r/ within the subreddit)"
        ),
        filters: Option(str, "New, Hot, or Rising", choices=["New", "Hot", "Rising"]),
    ):
        """Returns up to 25 reddit posts based on the current filter"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="alpine:rin:v2.2.4 (by /u/No767)",
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
                            value=datetime.datetime.fromtimestamp(
                                submission.created_utc
                            ).strftime("%Y-%m-%d %H:%M"),
                            inline=True,
                        )
                        .add_field(
                            name="Created At (UTC, 12hr or AM/PM)",
                            value=datetime.datetime.fromtimestamp(
                                submission.created_utc
                            ).strftime("%Y-%m-%d %I:%M %p"),
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

    @redditUsers.command(name="info")
    async def redditor(self, ctx, *, redditor: Option(str, "The name of the Redditor")):
        """Provides info about a Redditor"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="alpine:rin:v2.2.4 (by /u/No767)",
        ) as redditorApi:
            user = redditor
            try:
                try:
                    if "u/" in str(redditor):
                        userSplit = str(redditor).split("/")
                        user = userSplit[1]
                    mainUser = await redditorApi.redditor(user)
                    await mainUser.load()
                    embedVar = discord.Embed()
                    embedVar.title = mainUser.name
                    embedVar.set_thumbnail(url=mainUser.icon_img)
                    embedVar.add_field(
                        name="Comment Karma", value=mainUser.comment_karma, inline=True
                    )
                    embedVar.add_field(
                        name="Created At (UTC, 24hr)",
                        value=datetime.datetime.fromtimestamp(
                            mainUser.created_utc
                        ).strftime("%Y-%m-%d %H:%M"),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Created At (UTC, 12hr or AM/PM)",
                        value=datetime.datetime.fromtimestamp(
                            mainUser.created_utc
                        ).strftime("%Y-%m-%d %I:%M %p"),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Link Karma", value=mainUser.link_karma, inline=True
                    )
                    await ctx.respond(embed=embedVar)
                except NotFound:
                    notFoundError = discord.Embed()
                    notFoundError.description = (
                        "The user requested could not be found. Please try again"
                    )
                    await ctx.respond(embed=notFoundError)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again..."
                embedError.add_field(
                    name="Error Message",
                    value=f"{e.__module__}.{e.__class__.__name__}: {str(e)}",
                    inline=True,
                )
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @redditUsers.command(name="comments")
    async def redditorComments(
        self, ctx, *, redditor: Option(str, "The name of the Redditor")
    ):
        """Returns up to 25 comments from a given Redditor"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="alpine:rin:v2.2.4 (by /u/No767)",
        ) as redditorCommentsAPI:
            user = redditor
            try:
                try:
                    if "u/" in str(redditor):
                        userSplit = str(redditor).split("/")
                        user = userSplit[1]
                    userComment = await redditorCommentsAPI.redditor(user)
                    idealPage2 = [
                        discord.Embed(
                            title=comment.author.name, description=comment.body
                        )
                        .add_field(
                            name="Created At (UTC, 24hr)",
                            value=datetime.datetime.fromtimestamp(
                                comment.created_utc
                            ).strftime("%Y-%m-%d %H:%M"),
                            inline=True,
                        )
                        .add_field(
                            name="Created At (UTC, 12hr or AM/PM)",
                            value=datetime.datetime.fromtimestamp(
                                comment.created_utc
                            ).strftime("%Y-%m-%d %I:%M %p"),
                            inline=True,
                        )
                        .add_field(name="Score", value=comment.score, inline=True)
                        .add_field(
                            name="Subreddit",
                            value=comment.subreddit.display_name,
                            inline=True,
                        )
                        .add_field(
                            name="Original Post Link",
                            value=f"https://reddit.com/r/{comment.subreddit.display_name}/comments/{comment.submission.id}",
                            inline=True,
                        )
                        .add_field(
                            name="Link",
                            value=f"https://reddit.com{comment.permalink}",
                            inline=True,
                        )
                        .add_field(name="Edited", value=comment.edited, inline=True)
                        async for comment in userComment.comments.new(limit=25)
                    ]
                    mainPages = pages.Paginator(pages=idealPage2, loop_pages=True)
                    await mainPages.respond(ctx.interaction, ephemeral=False)
                except NotFound:
                    notFoundError = discord.Embed()
                    notFoundError.description = (
                        "The user requested could not be found. Please try again"
                    )
                    await ctx.respond(embed=notFoundError)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again..."
                embedError.add_field(
                    name="Error Message",
                    value=f"{e.__module__}.{e.__class__.__name__}: {str(e)}",
                    inline=True,
                )
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="egg_irl")
    async def redditEgg(
        self,
        ctx,
        filters: Option(str, "New, Top or Hot", choices=["New", "Top", "Rising"]),
    ):
        """Literally just shows you r/egg_irl posts. No comment."""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="alpine:rin:v2.2.4 (by /u/No767)",
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
                            value=datetime.datetime.fromtimestamp(
                                submission.created_utc
                            ).strftime("%Y-%m-%d %H:%M"),
                            inline=True,
                        )
                        .add_field(
                            name="Created At (UTC, 12hr or AM/PM)",
                            value=datetime.datetime.fromtimestamp(
                                submission.created_utc
                            ).strftime("%Y-%m-%d %I:%M %p"),
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


def setup(bot):
    bot.add_cog(RedditV1(bot))
