import os

import discord
import tweepy
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Access the Twitter API via Tweepy
Twitter_API_Key = os.getenv("Twitter_API_Key")
API_Secret_Key = os.getenv("API_Secret_Key")
Access_Token = os.getenv("Access_Token")
Access_Token_Secret = os.getenv("Access_Token_Secret")
Bearer_Token = os.getenv("Twitter_Bearer_Token")

auth = tweepy.Client(bearer_token=Bearer_Token, consumer_key=Twitter_API_Key, consumer_secret=API_Secret_Key, access_token=Access_Token, access_token_secret=Access_Token_Secret)

api = tweepy.API(auth)


class rintwitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rt")
    async def rintwitter(self, ctx):
        home_timeline = api.mentions_timeline()
        embedVar = discord.Embed()
        embedVar.description = f"Current Timeline: {home_timeline}"
        await ctx.send(embed=embedVar)


class rtupdatestatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # The OAuth can only handle Read requests, not post requests. adding support in the future
    @commands.command(name="rtupdatestatus")
    async def on_message(self, ctx, search: str):
        twitter_query = api.update_status(status=search)
        twitter_embed = discord.Embed()
        twitter_embed.description = (
            f"Your Twitter Status has been updated to {twitter_query}"
        )
        await ctx.send(embed=twitter_embed)


class rtgetsaved(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Make sure that the search input is a string, by wrapping it in '' or ""
    @commands.command(name="rtsearch")
    async def rtgetsaved(self, ctx, *, search: str):
        getcursor = api.get_user(search)
        search_embed = discord.Embed()
        search_embed.description = f"{api.get_user(search)}"
        await ctx.send(embed=search_embed)


def setup(bot):
    bot.add_cog(rintwitter(bot))
    bot.add_cog(rtgetsaved(bot))
    bot.add_cog(rtupdatestatus(bot))
