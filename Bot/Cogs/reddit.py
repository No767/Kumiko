import asyncio
import os
import random

import asyncpraw
import discord
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from exceptions import ThereIsaRSlashInSubreddit

load_dotenv()

Reddit_ID = os.getenv("Reddit_ID")
Reddit_Secret = os.getenv("Reddit_Secret")


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
            user_agent="ubuntu:rin:v2.1.0 (by /u/No767)",
        ) as api:
            original_search = search
            try:
                if "r/" in search:
                    search = search.split("/")
                    sub = search[1]
                    search = "all"
                else:
                    sub = "all"
                sub = await api.subreddit(sub)
                searcher = sub.search(query=search)
                posts = [
                    post
                    async for post in searcher
                    if ".jpg" in post.url
                    or ".png" in post.url
                    or ".gif" in post.url
                    and not post.over_18
                ]
                post = random.choice(posts)  # nosec B311
                submission = post
                reddit_embed = discord.Embed(color=discord.Color.from_rgb(255, 69, 0))
                reddit_embed.description = f"{self.bot.user.name} found this post in r/{submission.subreddit.display_name} by {submission.author.name} when searching {original_search}"
                reddit_embed.set_image(url=submission.url)
                await ctx.respond(embed=reddit_embed)
            except Exception as e:
                embed = discord.Embed()
                embed.description = f"There was an error, this is likely caused by a lack of posts found in the query {original_search}. Please try again."
                embed.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="new")
    async def redditNew(
        self,
        ctx,
        *,
        subreddit: Option(
            str, "The subreddit to search (Don't include r/ within the subreddit)"
        ),
    ):
        """Returns up to 5 new posts from any given subreddit"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.1.0 (by /u/No767)",
        ) as redditapi:
            try:
                try:
                    if "r/" in subreddit:
                        raise ThereIsaRSlashInSubreddit
                    else:
                        mainSub = await redditapi.subreddit(subreddit)
                        async for submission in mainSub.new(limit=5):
                            await submission.author.load()
                            embedVar = discord.Embed()
                            embedVar.title = submission.title
                            embedVar.description = submission.selftext
                            embedVar.add_field(
                                name="Author", value=submission.author, inline=True
                            )
                            embedVar.add_field(
                                name="NSFW", value=submission.over_18, inline=True
                            )
                            embedVar.add_field(
                                name="Number of Upvotes",
                                value=submission.score,
                                inline=True,
                            )
                            embedVar.add_field(
                                name="ID", value=submission.id, inline=True
                            )
                            embedVar.add_field(
                                name="Flair",
                                value=submission.link_flair_text,
                                inline=True,
                            )
                            embedVar.set_image(url=submission.url)
                            embedVar.set_thumbnail(url=submission.author.icon_img)
                            await ctx.respond(embed=embedVar)
                except ThereIsaRSlashInSubreddit:
                    aFoolishMove = discord.Embed()
                    aFoolishMove.description = "Sorry, but you may have added the `r/` prefix of each subreddit. Please try again, but without the prefix"
                    await ctx.respond(embed=aFoolishMove)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = f"There was an error, this is likely caused by a lack of posts found in the query {subreddit}. Please try again."
                embedError.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="comments")
    async def redditComments(self, ctx, *, post_id: Option(str, "ID of post")):
        """Returns up to 10 comments from a given post ID"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.1.0 (by /u/No767)",
        ) as api:
            try:
                post = await api.submission(id=post_id)
                mainComments = await post.comments()
                embedVar = discord.Embed()
                for item in mainComments:
                    await item.author.load()
                    embedVar.title = item.author.name
                    embedVar.description = item.body
                    embedVar.add_field(name="Upvotes", value=item.score, inline=True)
                    embedVar.set_thumbnail(url=item.author.icon_img)
                    embedVar.remove_field(1)
                    await ctx.respond(embed=embedVar)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again..."
                embedError.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @redditUsers.command(name="info")
    async def redditor(self, ctx, *, redditor: Option(str, "The name of the Redditor")):
        """Provides info about a Redditor"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.1.0 (by /u/No767)",
        ) as redditorApi:
            try:
                user = await redditorApi.redditor(redditor)
                await user.load()
                embedVar = discord.Embed()
                embedVar.title = user.name
                embedVar.set_thumbnail(url=user.icon_img)
                embedVar.add_field(
                    name="Comment Karma", value=user.comment_karma, inline=True
                )
                embedVar.add_field(
                    name="Created UTC", value=user.created_utc, inline=True
                )
                embedVar.add_field(
                    name="Link Karma", value=user.link_karma, inline=True
                )
                await ctx.respond(embed=embedVar)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again..."
                embedError.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @redditUsers.command(name="comments")
    async def redditorComments(
        self, ctx, *, redditor: Option(str, "The name of the Redditor")
    ):
        """Returns up to 10 comments from a given Redditor"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.1.0 (by /u/No767)",
        ) as redditorCommentsAPI:
            try:
                userComment = await redditorCommentsAPI.redditor(redditor)
                embedVar = discord.Embed()
                async for comment in userComment.comments.new(limit=10):
                    await comment.author.load()
                    embedVar.title = comment.author.name
                    embedVar.description = comment.body
                    embedVar.set_thumbnail(url=comment.author.icon_img)
                    await ctx.respond(embed=embedVar)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = "Something went wrong. Please try again... (More than likely you may have used the wrong redditor...)"
                embedError.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="hot")
    async def redditHot(
        self,
        ctx,
        *,
        subreddit: Option(
            str, "The subreddit to search (Don't include r/ within the subreddit)"
        ),
    ):
        """Returns up to 5 hot posts from any subreddit"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.1.0 (by /u/No767)",
        ) as redditapi:
            if "r/" in subreddit:
                subParser = subreddit.split("/")
                sub = subParser[1]
            else:
                sub = subreddit
            mainSub = await redditapi.subreddit(sub)
            try:
                try:
                    if "r/" in subreddit:
                        raise ThereIsaRSlashInSubreddit
                    else:
                        mainSub = await redditapi.subreddit(subreddit)
                        async for submission in mainSub.hot(limit=5):
                            await submission.author.load()
                            embedVar = discord.Embed()
                            embedVar.title = submission.title
                            embedVar.description = submission.selftext
                            embedVar.add_field(
                                name="Author", value=submission.author, inline=True
                            )
                            embedVar.add_field(
                                name="NSFW", value=submission.over_18, inline=True
                            )
                            embedVar.add_field(
                                name="Number of Upvotes",
                                value=submission.score,
                                inline=True,
                            )
                            embedVar.add_field(
                                name="ID", value=submission.id, inline=True
                            )
                            embedVar.add_field(
                                name="Flair",
                                value=submission.link_flair_text,
                                inline=True,
                            )
                            embedVar.set_image(url=submission.url)
                            embedVar.set_thumbnail(url=submission.author.icon_img)
                            await ctx.respond(embed=embedVar)
                except ThereIsaRSlashInSubreddit:
                    aFoolishMove = discord.Embed()
                    aFoolishMove.description = "Sorry, but you may have added the `r/` prefix of each subreddit. Please try again, but without the prefix"
                    await ctx.respond(embed=aFoolishMove)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = f"There was an error, this is likely caused by a lack of posts found in the query {subreddit}. Please try again."
                embedError.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="top")
    async def redditTop(
        self,
        ctx,
        *,
        subreddit: Option(
            str, "The subreddit to search (Don't include r/ within the subreddit)"
        ),
    ):
        """Returns 5 top posts from any subreddit"""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.1.0 (by /u/No767)",
        ) as redditapi:
            try:
                try:
                    if "r/" in subreddit:
                        raise ThereIsaRSlashInSubreddit
                    else:
                        mainSub = await redditapi.subreddit(subreddit)
                        async for submission in mainSub.top(limit=5):
                            await submission.author.load()
                            embedVar = discord.Embed()
                            embedVar.title = submission.title
                            embedVar.description = submission.selftext
                            embedVar.add_field(
                                name="Author", value=submission.author, inline=True
                            )
                            embedVar.add_field(
                                name="NSFW", value=submission.over_18, inline=True
                            )
                            embedVar.add_field(
                                name="Number of Upvotes",
                                value=submission.score,
                                inline=True,
                            )
                            embedVar.add_field(
                                name="ID", value=submission.id, inline=True
                            )
                            embedVar.add_field(
                                name="Flair",
                                value=submission.link_flair_text,
                                inline=True,
                            )
                            embedVar.set_image(url=submission.url)
                            embedVar.set_thumbnail(url=submission.author.icon_img)
                            await ctx.respond(embed=embedVar)
                except ThereIsaRSlashInSubreddit:
                    aFoolishMove = discord.Embed()
                    aFoolishMove.description = "Sorry, but you may have added the `r/` prefix of each subreddit. Please try again, but without the prefix"
                    await ctx.respond(embed=aFoolishMove)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = f"There was an error, this is likely caused by a lack of posts found in the query {subreddit}. Please try again."
                embedError.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.command(name="egg_irl")
    async def redditEgg(
        self,
        ctx,
        filters: Option(str, "New, Top or Hot", choices=["new", "top", "hot"]),
    ):
        """Literally just shows you r/egg_irl posts."""
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.1.0 (by /u/No767)",
        ) as redditapi:
            try:
                mainSub = await redditapi.subreddit("egg_irl")
                if "new" in filters:
                    subLooper = mainSub.new(limit=25)
                elif "top" in filters:
                    subLooper = mainSub.top(limit=25)
                elif "hot" in filters:
                    subLooper = mainSub.hot(limit=25)
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=submission.title, description=submission.selftext
                        )
                        .add_field(name="NSFW", value=submission.over_18, inline=True)
                        .add_field(
                            name="Number of Upvotes",
                            value=submission.score,
                            inline=True,
                        )
                        .add_field(name="ID", value=submission.id, inline=True)
                        .add_field(
                            name="Flair", value=submission.link_flair_text, inline=True
                        )
                        .set_image(url=submission.url)
                        async for submission in subLooper
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=False)
            except Exception as e:
                embedError = discord.Embed()
                embedError.description = f"There was an error, this is likely caused by a lack of posts found in the query. Please try again."
                embedError.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedError)


def setup(bot):
    bot.add_cog(RedditV1(bot))
