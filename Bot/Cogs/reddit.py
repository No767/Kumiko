from discord.ext import commands
import discord
import random
import praw
from dotenv import load_dotenv
import os

load_dotenv()

# Replaced the old user input based auth with a more secure env var based auth
# Make sure you have this stored at the same directory as the rinbot file within a .env file
reddit_id = os.getenv("Reddit_ID")
reddit_secret = os.getenv("Reddit_Secret")

redditapi = praw.Reddit(
    client_id=f'{os.getenv("Reddit_ID")}',
    client_secret=f'{os.getenv("Reddit_Secret")}',
    # the user_agent just identifies to reddit what browser it's connecting from.
    user_agent="Discord",
    # asyncpraw is causing issues and will be worked upon
    check_for_async=False,
)


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

    @commands.command(name="reddit", help="browses on reddit")
    async def reddit(self, ctx, *, search: str):
        original_search = search
        try:
            if "r/" in search:
                # treat as subreddit
                search = search.split("/")
                sub = search[1]
                search = "all"
            else:
                # treat as general search
                sub = "all"
            # query reddit for posts
            redditquery = redditapi.subreddit(sub).search(search)
            # looks for a suitable posts
            posts = [
                post
                for post in redditquery
                if ".jpg" in post.url
                or ".png" in post.url
                or ".gif" in post.url
                and not post.over_18
            ]
            # ensuring random post
            post = random.choice(posts)
            # finding a suitable post
            submission = post
            # discord embed setup
            reddit_embed = discord.Embed()
            reddit_embed.description = f"{self.bot.user.name} found this post in r/{submission.subreddit.display_name} by {submission.author.name} when searching {original_search}"
            reddit_embed.set_image(url=submission.url)
            await ctx.send(embed=reddit_embed)
            return
        except:
            await ctx.send(
                f"There was an error, this is likely caused by a lack of posts found in the query {original_search}. Please try again."
            )


def setup(bot):
    bot.add_cog(reddit(bot))
