import os

import discord
import spotipy
from discord.ext import commands
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
import uvloop

load_dotenv()

Spotify_Client_ID = os.getenv("Spotify_Client_ID")
Spotify_Client_Secret = os.getenv("Spotify_Client_Secret")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=Spotify_Client_ID, client_secret=Spotify_Client_Secret
    )
)


def get_album_of_track(search):
    return sp.search(q=search, type="album", limit=1)


class SpotifyV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="spotify-search-album", aliases=["sp-search-album"])
    async def search(self, ctx, *, search: str):
        try:
            res = get_album_of_track(search)
            embedVar = discord.Embed(title=res["albums"]["items"][0]["name"])
            embedVar.add_field(
                name="Artist",
                value=res["albums"]["items"][0]["artists"][0]["name"],
                inline=True,
            )
            embedVar.add_field(
                name="Release Date",
                value=res["albums"]["items"][0]["release_date"],
                inline=True,
            )
            embedVar.add_field(
                name="Total Tracks",
                value=res["albums"]["items"][0]["total_tracks"],
                inline=True,
            )
            embedVar.set_thumbnail(
                url=res["albums"]["items"][0]["images"][0]["url"])
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.add_field(name="Error", value=e, inline=False)
            await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @search.error
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
    bot.add_cog(SpotifyV1(bot))
