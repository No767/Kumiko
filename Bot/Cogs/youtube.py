import asyncio
import os

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

YouTube_API_Key = os.getenv("YouTube_API_Key")

jsonParser = simdjson.Parser()


class YoutubeV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    yt = SlashCommandGroup("youtube", "Commands for the YouTube service")

    @yt.command(name="search")
    async def youtube_search(self, ctx, *, search: Option(str, "Video Search Term")):
        """Finds up to 25 videos on YouTube based on the given search term"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": YouTube_API_Key,
                "part": "snippet",
                "type": "video",
                "maxResults": "25",
                "q": search,
                "channelType": "any",
                "videoLicense": "any",
                "safeSearch": "strict",
            }
            async with session.get(
                "https://www.googleapis.com/youtube/v3/search", params=params
            ) as r:
                data = await r.content.read()
                dataMain = jsonParser.parse(data, recursive=True)
                try:
                    if len(dataMain["items"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=dictItem["snippet"]["title"],
                                    description=dictItem["snippet"]["description"],
                                    color=discord.Color.from_rgb(212, 255, 223),
                                )
                                .add_field(
                                    name="Channel",
                                    value=dictItem["snippet"]["channelTitle"],
                                )
                                .add_field(
                                    name="Published At (24hr)",
                                    value=parser.isoparse(
                                        dictItem["snippet"]["publishedAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Published At (12 hr)",
                                    value=parser.isoparse(
                                        dictItem["snippet"]["publishedAt"]
                                    ).strftime("%Y-%m-%d %I:%M:%S %p"),
                                    inline=True,
                                )
                                .add_field(
                                    name="YouTube Video Link",
                                    value=f'https://youtube.com/watch?v={dictItem["id"]["videoId"]}',
                                    inline=True,
                                )
                                .set_image(
                                    url=dictItem["snippet"]["thumbnails"]["high"]["url"]
                                )
                                for dictItem in dataMain["items"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedValError = discord.Embed()
                    embedValError.description = (
                        "It seems like that search term didn't work.... 😭"
                    )
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @yt.command(name="channel")
    async def youtube_channel(self, ctx, *, channel: Option(str, "Channel Name")):
        """Returns info about the given YouTube channel"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            search_params = {
                "key": YouTube_API_Key,
                "part": "snippet",
                "type": "channel",
                "maxResults": "1",
                "q": channel,
                "channelType": "any",
                "videoLicense": "any",
                "order": "relevance",
            }
            async with session.get(
                "https://www.googleapis.com/youtube/v3/search", params=search_params
            ) as response:
                search_data = await response.content.read()
                searchDataMain = jsonParser.parse(search_data, recursive=True)
                try:
                    if len(searchDataMain["items"]) == 0:
                        raise NoItemsError
                    else:
                        channel_id = searchDataMain["items"][0]["id"]["channelId"]
                        params = {
                            "key": YouTube_API_Key,
                            "part": "snippet,statistics",
                            "id": channel_id,
                        }
                        async with session.get(
                            "https://www.googleapis.com/youtube/v3/channels",
                            params=params,
                        ) as re:
                            data = await re.content.read()
                            dataMain3 = jsonParser.parse(data, recursive=True)
                            try:
                                embedVar = discord.Embed(
                                    color=discord.Color.from_rgb(255, 0, 0)
                                )
                                filterMain5 = {
                                    "kind",
                                    "etag",
                                    "snippet",
                                    "statistics",
                                    "localized",
                                    "id",
                                }
                                snippetFilter = [
                                    "title",
                                    "description",
                                    "thumbnails",
                                    "localized",
                                    "id",
                                    "publishedAt",
                                ]
                                if len(dataMain3["items"]) == 0:
                                    raise ValueError
                                else:
                                    for dictItem in dataMain3["items"]:
                                        for key, val in dictItem.items():
                                            if key not in filterMain5:
                                                embedVar.add_field(
                                                    name=key, value=val, inline=True
                                                )
                                        for k, v in dictItem["snippet"].items():
                                            if k not in snippetFilter:
                                                embedVar.add_field(
                                                    name=k, value=v, inline=True
                                                )
                                        for keys, value in dictItem[
                                            "statistics"
                                        ].items():
                                            embedVar.add_field(
                                                name=keys, value=value, inline=True
                                            )
                                        embedVar.add_field(
                                            name="publishedAt",
                                            value=parser.isoparse(
                                                dictItem["snippet"]["publishedAt"]
                                            ).strftime("%Y-%m-%d %H:%M:%S"),
                                            inline=True,
                                        )
                                        embedVar.add_field(
                                            name="channel_url",
                                            value=f'https://youtube.com/channel/{dictItem["id"]}',
                                            inline=True,
                                        )
                                        embedVar.title = dictItem["snippet"]["title"]
                                        embedVar.description = dictItem["snippet"][
                                            "description"
                                        ]
                                        embedVar.set_thumbnail(
                                            url=dictItem["snippet"]["thumbnails"][
                                                "high"
                                            ]["url"]
                                        )
                                        await ctx.respond(embed=embedVar)
                            except ValueError:
                                embedError = discord.Embed()
                                embedError.description = f"No results found for {channel}. Please try again..."
                                await ctx.respond(embed=embedError)
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = (
                        f"No results found for {channel}. Please try again..."
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @yt.command(name="playlist")
    async def youtube_playlists(
        self, ctx, *, channel_name: Option(str, "Channel Name")
    ):
        """Returns up to 25 YouTube playlists based on the given YT channel"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            search_params = {
                "key": YouTube_API_Key,
                "part": "snippet",
                "type": "playlists",
                "maxResults": "1",
                "q": channel_name,
            }
            async with session.get(
                "https://www.googleapis.com/youtube/v3/search", params=search_params
            ) as response2:
                search_data = await response2.content.read()
                searchDataMain = jsonParser.parse(search_data, recursive=True)
                try:
                    if len(searchDataMain["items"]) == 0:
                        raise NoItemsError
                    else:
                        channel_id = searchDataMain["items"][0]["id"]["channelId"]
                        main_params = {
                            "key": YouTube_API_Key,
                            "part": "snippet,contentDetails",
                            "channelId": channel_id,
                            "maxResults": 25,
                        }
                        async with session.get(
                            "https://www.googleapis.com/youtube/v3/playlists",
                            params=main_params,
                        ) as r2:
                            data = await r2.content.read()
                            dataMain = jsonParser.parse(data, recursive=True)
                            try:
                                if len(dataMain["items"]) == 0:
                                    raise ValueError
                                else:
                                    playlistsPages = pages.Paginator(
                                        pages=[
                                            discord.Embed(
                                                title=mainItems["snippet"]["title"],
                                                description=mainItems["snippet"][
                                                    "description"
                                                ],
                                                color=discord.Color.from_rgb(
                                                    255, 224, 224
                                                ),
                                            )
                                            .add_field(
                                                name="Channel",
                                                value=mainItems["snippet"][
                                                    "channelTitle"
                                                ],
                                                inline=True,
                                            )
                                            .add_field(
                                                name="Item Count",
                                                value=mainItems["contentDetails"][
                                                    "itemCount"
                                                ],
                                                inline=True,
                                            )
                                            .add_field(
                                                name="Published At (24 hr)",
                                                value=parser.isoparse(
                                                    mainItems["snippet"]["publishedAt"]
                                                ).strftime("%Y-%m-%d %H:%M:%S"),
                                                inline=True,
                                            )
                                            .add_field(
                                                name="Published At (12 hr, AM/PM)",
                                                value=parser.isoparse(
                                                    mainItems["snippet"]["publishedAt"]
                                                ).strftime("%Y-%m-%d %I:%M:%S %p"),
                                                inline=True,
                                            )
                                            .add_field(
                                                name="YT Playlist URL",
                                                value=f'https://youtube.com/playlist?list={mainItems["id"]}',
                                                inline=True,
                                            )
                                            .set_image(
                                                url=mainItems["snippet"]["thumbnails"][
                                                    "maxres"
                                                ]["url"]
                                            )
                                            for mainItems in dataMain["items"]
                                        ],
                                        loop_pages=True,
                                    )
                                    await playlistsPages.respond(
                                        ctx.interaction, ephemeral=False
                                    )
                            except ValueError:
                                embedError = discord.Embed()
                                embedError.description = f"No results found for {channel_name}. Please try again..."
                                await ctx.respond(embed=embedError)
                except NoItemsError:
                    embedError = discord.Embed()
                    embedError.description = (
                        f"No results found for {channel_name}. Please try again..."
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # This command will stay commented out since this command
    # has been tested to work, but would kinda annoy folks
    # who would want to use it. And probably would annoy discord labs

    # @yt.command(name="video")
    # async def youtube_video(self, ctx, *, video_id: Option(str, "YT Video ID")):
    #     """Returns some info on the given YouTube video."""
    #     async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
    #         params = {
    #             "key": YouTube_API_Key,
    #             "part": "snippet,status,statistics",
    #             "id": video_id,
    #             "maxResults": 1,
    #         }
    #         async with session.get(
    #             "https://www.googleapis.com/youtube/v3/videos", params=params
    #         ) as another_response:
    #             data = await another_response.content.read()
    #             dataMain5 = jsonParser.parse(data, recursive=True)
    #             try:
    #
    #                 embed = discord.Embed(color=discord.Color.from_rgb(255, 0, 0))
    #                 snippetFilter = ["title", "description", "thumbnails", "localized"]
    #                 picFilter = ["default", "medium", "high", "standard"]
    #                 if len(dataMain5["items"]) == 0:
    #                     raise ValueError
    #                 else:
    #                     for items in dataMain5["items"]:
    #                         for keys, val in items["snippet"].items():
    #                             if keys not in snippetFilter:
    #                                 embed.add_field(name=keys, value=val, inline=True)
    #                         embed.title = items["snippet"]["title"]
    #                         embed.description = items["snippet"]["description"]
    #                         for key, value in items["statistics"].items():
    #                             embed.add_field(name=key, value=value, inline=True)
    #                         for k, v in items["snippet"]["thumbnails"].items():
    #                             if k not in picFilter:
    #                                 embed.set_image(url=v["url"])
    #                     await ctx.respond(embed=embed)
    #             except ValueError:
    #                 embedError = discord.Embed()
    #                 embedError.description = "Sorry, it seems like there wasn't any results... Please try again"
    #                 await ctx.respond(embed=embedError)
    #
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(YoutubeV1(bot))
