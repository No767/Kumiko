import asyncio
import os
import urllib.parse

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from rin_exceptions import NoItemsError

load_dotenv()

TWITCH_API_KEY = os.getenv("Twitch_API_Access_Token")
TWITCH_CLIENT_ID = os.getenv("Twitch_API_Client_ID")

jsonParser = simdjson.Parser()


class TwitchV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    twitch = SlashCommandGroup("twitch", "Twitch commands")
    twitchSearch = twitch.create_subgroup("search", "Search for stuff on Twitch")
    twitchTop = twitch.create_subgroup("top", "Top stuff on Twitch")

    @twitch.command(name="streams")
    async def getActiveStreams(self, ctx):
        """Gets up to 25 active streams on Twitch"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"Bearer {TWITCH_API_KEY}",
                "Client-Id": TWITCH_CLIENT_ID,
            }
            params = {"first": 25}
            async with session.get(
                "https://api.twitch.tv/helix/streams", headers=headers, params=params
            ) as r:
                data = await r.content.read()
                dataMain = jsonParser.parse(data, recursive=True)
                try:
                    if len(dataMain["data"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(title=mainItem["title"])
                                .add_field(
                                    name="Game Name",
                                    value=mainItem["game_name"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Streamer",
                                    value=mainItem["user_name"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Viewer Count",
                                    value=mainItem["viewer_count"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Started At",
                                    value=parser.isoparse(
                                        mainItem["started_at"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Type", value=mainItem["type"], inline=True
                                )
                                .add_field(
                                    name="Is Mature",
                                    value=mainItem["is_mature"],
                                    inline=True,
                                )
                                .set_image(
                                    url=str(mainItem["thumbnail_url"]).replace(
                                        "{width}x{height}", "1920x1080"
                                    )
                                )
                                for mainItem in dataMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = "Sadly there are no streams active at the moment. Please try again"
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @twitchSearch.command(name="channels")
    async def getTwitchChannels(
        self, ctx, *, channel: Option(str, "The name of the channel")
    ):
        """Returns up to 25 streams from the given channel"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"Bearer {TWITCH_API_KEY}",
                "Client-Id": TWITCH_CLIENT_ID,
            }
            params = {"first": 25, "query": urllib.parse.quote(channel)}
            async with session.get(
                "https://api.twitch.tv/helix/search/channels",
                headers=headers,
                params=params,
            ) as r:
                data = await r.content.read()
                dataMain = jsonParser.parse(data, recursive=True)
                try:
                    if len(dataMain["data"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=f'{mainItem["display_name"]} - {mainItem["title"]}'
                                )
                                .add_field(
                                    name="Game Name",
                                    value=f'[{mainItem["game_name"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Is Live",
                                    value=mainItem["is_live"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Broadcaster Language",
                                    value=f'[{mainItem["broadcaster_language"]}]',
                                    inline=True,
                                )
                                .set_thumbnail(url=mainItem["thumbnail_url"])
                                for mainItem in dataMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sadly there are no streams on this channel. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @twitchTop.command(name="games")
    async def getTopGames(self, ctx):
        """Gets the top 100 games on Twitch"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "Authorization": f"Bearer {TWITCH_API_KEY}",
                "Client-Id": TWITCH_CLIENT_ID,
            }
            params = {"first": 100}
            async with session.get(
                "https://api.twitch.tv/helix/games/top", headers=headers, params=params
            ) as r:
                data = await r.content.read()
                dataMain = jsonParser.parse(data, recursive=True)
                try:
                    if len(dataMain["data"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(title=mainItem["name"])
                                .add_field(
                                    name="Twitch Game ID",
                                    value=mainItem["id"],
                                    inline=True,
                                )
                                .set_thumbnail(
                                    url=str(mainItem["box_art_url"]).replace(
                                        "{width}x{height}", "512x512"
                                    )
                                )
                                for mainItem in dataMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sadly there are no top games as of now. Please try again"
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(TwitchV1(bot))
