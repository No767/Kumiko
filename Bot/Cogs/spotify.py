import os
import sys

import discord
import spotipy
from discord.ext import commands
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

load_dotenv()

Spotify_Client_ID = os.getenv("Spotify_Client_ID")
Spotify_Client_Secret = os.getenv("Spotify_Client_Secret")
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(
    client_credentials_manager=SpotifyOAuth(
        scope=scope,
        client_id=Spotify_Client_ID,
        client_secret=Spotify_Client_Secret,
        redirect_uri="https://github.com/No767/Rin",
    )
)


class SpotifyV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rinplay")
    async def play(self, ctx):
        voicechannel = discord.utils.get(ctx.guild.voice_channels)
        vc = await voicechannel.connect()
        vc.play(
            sp.start_playback(
                uris=[
                    "https://open.spotify.com/track/1NIjnTO2M2Vjgc2UrotvSz?si=6c51908d0e684982"
                ]
            )
        )


def setup(bot):
    bot.add_cog(SpotifyV1(bot))
