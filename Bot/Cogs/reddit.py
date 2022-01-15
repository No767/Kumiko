import asyncio
import os
import random

import asyncpraw
import discord
import uvloop
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Replaced the old user input based auth with a more secure env var based auth
# Make sure you have this stored at the same directory as the rinbot file within a .env file
Reddit_ID = os.getenv("Reddit_ID")
Reddit_Secret = os.getenv("Reddit_Secret")


class reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme", help="finds a meme")
    async def meme(self, ctx):
        searchtopics = [
            " ",
            "dank",
            "anime",
            "christian",
            "tech ",
            "funny ",
            "coding ",
            "reddit ",
            "music ",
            "manga ",
            "school ",
            "relatable ",
        ]
        searchterm = random.choice(searchtopics) + "memes"
        await ctx.invoke(self.bot.get_command("reddit"), search=searchterm)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @commands.command(name="transmeme", help="finds a trans related meme")
    async def transmeme(self, ctx):
        # Tried to watch onetopic in order to figure out the different subs
        searchtopics = [
            " ",
            " trans ",
            " egg_irl ",
            " traaaaaaannnnnnnnnns ",
            " GaySoundsShitposts ",
            " Bisexual ",
            " Bi_IRL ",
            " ActualLesbians ",
            " SapphoAndherFriend",
        ]
        searchterm = random.choice(searchtopics)
        await ctx.invoke(self.bot.get_command("reddit"), search=searchterm)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @commands.command(name="reddit", help="browses on reddit")
    async def reddit(self, ctx, *, search: str):
        async with asyncpraw.Reddit(
            client_id=Reddit_ID,
            client_secret=Reddit_Secret,
            user_agent="ubuntu:rin:v1.4.0-dev (by /u/No767)",
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
                await ctx.send(embed=reddit_embed)
            except Exception as e:
                embed = discord.Embed()
                embed.description = f"There was an error, this is likely caused by a lack of posts found in the query {original_search}. Please try again."
                embed.add_field(name="Reason", value=e, inline=True)
                await ctx.send(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @reddit.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(reddit(bot))
