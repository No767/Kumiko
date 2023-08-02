import os
from datetime import datetime
from typing import Literal, Optional

import asyncpraw
import orjson
from discord import PartialEmoji, app_commands
from discord.ext import commands
from discord.utils import format_dt
from dotenv import load_dotenv
from kumikocore import KumikoCore
from Libs.utils import parseSubreddit
from Libs.utils.pages import EmbedListSource, KumikoPages

load_dotenv()


REDDIT_ID = os.environ["REDDIT_ID"]
REDDIT_SECRET = os.environ["REDDIT_SECRET"]


class Reddit(commands.Cog):
    """Search, and view posts and memes from Reddit"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<:reddit:314349923103670272>")

    @commands.hybrid_group(name="reddit")
    async def reddit(self, ctx: commands.Context) -> None:
        """Reddit search and utility commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @reddit.command(name="search")
    @app_commands.describe(
        search="The search query to use",
        subreddit="Which subreddit to use. Defaults to all.",
    )
    async def search(
        self, ctx: commands.Context, *, search: str, subreddit: Optional[str] = "all"
    ) -> None:
        """Searches for posts on Reddit"""
        async with asyncpraw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="Kumiko (by /u/No767)",
            requestor_kwargs={"session": self.bot.session},
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

    @reddit.command(name="feed")
    @app_commands.describe(
        subreddit="Subreddit to search", filter="Sort filters. Defaults to New"
    )
    async def feed(
        self,
        ctx: commands.Context,
        subreddit: str,
        filter: Optional[Literal["New", "Hot", "Rising"]] = "New",
    ) -> None:
        """Gets a feed of posts from a subreddit"""
        async with asyncpraw.Reddit(
            client_id=REDDIT_ID,
            client_secret=REDDIT_SECRET,
            user_agent="Kumiko (by /u/No767)",
            requestor_kwargs={"session": self.bot.session},
        ) as reddit:
            sub = await reddit.subreddit(parseSubreddit(subreddit))
            subGen = (
                sub.new(limit=10)
                if filter == "New"
                else sub.hot(limit=10)
                if filter == "Hot"
                else sub.rising(limit=10)
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

    @reddit.command(name="memes")
    @app_commands.describe(
        subreddit="Subreddit to search",
        amount="Amount of memes to return. Defaults to 5",
    )
    async def search_memes(
        self, ctx: commands.Context, subreddit: str, amount: Optional[int] = 5
    ) -> None:
        """Searches for memes on Reddit"""
        async with self.bot.session.get(
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


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Reddit(bot))
