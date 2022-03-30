import asyncio
import os
import random

import asyncpraw
import discord
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

Reddit_ID = os.getenv("Reddit_ID")
Reddit_Secret = os.getenv("Reddit_Secret")


class RedditV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="reddit",
        description="Searches on reddit for content",
    )
    async def reddit(
        self,
        ctx,
        *,
        search: Option(
            str,
            "The query you want to search. Also supports searching subreddits as well",
        ),
    ):
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.0.0 (by /u/No767)",
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
                post = random.choice(posts)
                submission = post
                reddit_embed = discord.Embed(
                    color=discord.Color.from_rgb(255, 69, 0))
                reddit_embed.description = f"{self.bot.user.name} found this post in r/{submission.subreddit.display_name} by {submission.author.name} when searching {original_search}"
                reddit_embed.set_image(url=submission.url)
                await ctx.respond(embed=reddit_embed)
            except Exception as e:
                embed = discord.Embed()
                embed.description = f"There was an error, this is likely caused by a lack of posts found in the query {original_search}. Please try again."
                embed.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class RedditV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="reddit-new",
        description="Returns 5 new posts from any subreddit",
    )
    async def redditNew(
        self, ctx, *, subreddit: Option(str, "The subreddit to search")
    ):
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.0.0 (by /u/No767)",
        ) as redditapi:
            if "r/" in subreddit:
                subParser = subreddit.split("/")
                sub = subParser[1]
            else:
                sub = subreddit
            mainSub = await redditapi.subreddit(sub)
            async for submission in mainSub.new(limit=5):
                await submission.author.load()
                embedVar = discord.Embed()
                embedVar.title = submission.title
                embedVar.description = submission.selftext
                embedVar.add_field(
                    name="Author", value=submission.author, inline=True)
                embedVar.add_field(
                    name="Locked", value=submission.locked, inline=True)
                embedVar.add_field(
                    name="NSFW", value=submission.over_18, inline=True)
                embedVar.add_field(
                    name="Number of Upvotes", value=submission.score, inline=True
                )
                embedVar.add_field(
                    name="Spoiler", value=submission.spoiler, inline=True
                )
                embedVar.add_field(
                    name="Number of Comments",
                    value=submission.num_comments,
                    inline=True,
                )
                embedVar.set_image(url=submission.url)
                embedVar.set_thumbnail(url=submission.author.icon_img)
                await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class RedditV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="reddit-comments",
        description="Returns up to 10 comments from a given post ID",
    )
    async def redditComments(self, ctx, *, post_id: Option(str, "ID of post")):
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.0.0 (by /u/No767)",
        ) as api:
            post = await api.submission(id=post_id)
            comments = await post.comments()
            listedComments = await comments.list()
            embedVar = discord.Embed()
            for item in comments:
                if len(listedComments) > 10:
                    return
                else:
                    await item.author.load()
                    embedVar.title = item.author.name
                    embedVar.description = item.body
                    embedVar.add_field(
                        name="Upvotes", value=item.score, inline=True)
                    embedVar.set_thumbnail(url=item.author.icon_img)
                    embedVar.remove_field(1)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class RedditV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="reddit-user",
        description="Provides info about the given Redditor",
    )
    async def redditor(self, ctx, *, redditor: Option(str, "The name of the Redditor")):
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.0.0 (by /u/No767)",
        ) as redditorApi:
            user = await redditorApi.redditor(redditor)
            await user.load()
            embedVar = discord.Embed()
            embedVar.title = user.name
            embedVar.set_thumbnail(url=user.icon_img)
            embedVar.add_field(
                name="Comment Karma", value=user.comment_karma, inline=True
            )
            embedVar.add_field(name="Created UTC",
                               value=user.created_utc, inline=True)
            embedVar.add_field(name="Link Karma",
                               value=user.link_karma, inline=True)
            await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class RedditV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="reddit-user-comments",
        description="Returns up to 10 comments from a given Redditor",
    )
    async def redditorComments(
        self, ctx, *, redditor: Option(str, "The name of the Redditor")
    ):
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.0.0 (by /u/No767)",
        ) as redditorCommentsAPI:
            userComment = await redditorCommentsAPI.redditor(redditor)
            embedVar = discord.Embed()
            async for comment in userComment.comments.new(limit=10):
                await comment.author.load()
                embedVar.title = comment.author.name
                embedVar.description = comment.body
                embedVar.add_field(
                    name="Score", value=comment.score, inline=True)
                embedVar.add_field(
                    name="Created UTC", value=comment.created_utc, inline=True
                )
                embedVar.add_field(name="ID", value=comment.id, inline=True)
                embedVar.set_thumbnail(url=comment.author.icon_img)
                embedVar.remove_field(-3)
                await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class RedditV6(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="reddit-hot",
        description="Returns 5 hot posts from any subreddit",
    )
    async def redditNew(
        self, ctx, *, subreddit: Option(str, "The subreddit to search")
    ):
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.0.0 (by /u/No767)",
        ) as redditapi:
            if "r/" in subreddit:
                subParser = subreddit.split("/")
                sub = subParser[1]
            else:
                sub = subreddit
            mainSub = await redditapi.subreddit(sub)
            async for submission in mainSub.hot(limit=5):
                await submission.author.load()
                embedVar = discord.Embed()
                embedVar.title = submission.title
                embedVar.description = submission.selftext
                embedVar.add_field(
                    name="Author", value=submission.author, inline=True)
                embedVar.add_field(
                    name="Locked", value=submission.locked, inline=True)
                embedVar.add_field(
                    name="NSFW", value=submission.over_18, inline=True)
                embedVar.add_field(
                    name="Number of Upvotes", value=submission.score, inline=True
                )
                embedVar.add_field(
                    name="Spoiler", value=submission.spoiler, inline=True
                )
                embedVar.add_field(
                    name="Number of Comments",
                    value=submission.num_comments,
                    inline=True,
                )
                embedVar.set_image(url=submission.url)
                embedVar.set_thumbnail(url=submission.author.icon_img)
                await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class RedditV7(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="reddit-top",
        description="Returns 5 top posts from any subreddit",
    )
    async def redditNew(
        self, ctx, *, subreddit: Option(str, "The subreddit to search")
    ):
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v2.0.0 (by /u/No767)",
        ) as redditapi:
            if "r/" in subreddit:
                subParser = subreddit.split("/")
                sub = subParser[1]
            else:
                sub = subreddit
            mainSub = await redditapi.subreddit(sub)
            async for submission in mainSub.top(limit=5):
                await submission.author.load()
                embedVar = discord.Embed()
                embedVar.title = submission.title
                embedVar.description = submission.selftext
                embedVar.add_field(
                    name="Author", value=submission.author, inline=True)
                embedVar.add_field(
                    name="Locked", value=submission.locked, inline=True)
                embedVar.add_field(
                    name="NSFW", value=submission.over_18, inline=True)
                embedVar.add_field(
                    name="Number of Upvotes", value=submission.score, inline=True
                )
                embedVar.add_field(
                    name="Spoiler", value=submission.spoiler, inline=True
                )
                embedVar.add_field(
                    name="Number of Comments",
                    value=submission.num_comments,
                    inline=True,
                )
                embedVar.set_image(url=submission.url)
                embedVar.set_thumbnail(url=submission.author.icon_img)
                await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(RedditV1(bot))
    bot.add_cog(RedditV2(bot))
    bot.add_cog(RedditV3(bot))
    bot.add_cog(RedditV4(bot))
    bot.add_cog(RedditV5(bot))
    bot.add_cog(RedditV6(bot))
    bot.add_cog(RedditV7(bot))
