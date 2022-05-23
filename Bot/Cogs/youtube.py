import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from exceptions import NoItemsError

load_dotenv()

YouTube_API_Key = os.getenv("YouTube_API_Key")

parser = simdjson.Parser()


class YoutubeV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    yt = SlashCommandGroup("youtube", "Commands for the YouTube service")

    @yt.command(name="search")
    async def youtube_search(self, ctx, *, search: Option(str, "Video Search Term")):
        """Finds up to 5 videos on YouTube based on the given search term"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": YouTube_API_Key,
                "part": "snippet",
                "type": "video",
                "maxResults": "5",
                "q": search,
                "channelType": "any",
                "videoLicense": "any",
            }
            async with session.get(
                "https://www.googleapis.com/youtube/v3/search", params=params
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                try:
                    try:

                        if len(dataMain["items"]) == 0:
                            raise ValueError
                        else:
                            embedVar = discord.Embed(
                                color=discord.Color.from_rgb(212, 255, 223)
                            )
                            sizeFilter = ["default", "medium"]
                            itemFilter = [
                                "thumbnails",
                                "channelId",
                                "title",
                                "description",
                                "publishTime",
                            ]
                            for dictItem in dataMain["items"]:
                                for i, values in dictItem["snippet"][
                                    "thumbnails"
                                ].items():
                                    if i not in sizeFilter:
                                        embedVar.set_image(url=values["url"])

                                for items, val in dictItem["snippet"].items():
                                    if items not in itemFilter:
                                        embedVar.insert_field_at(
                                            index=1, name=items, value=val, inline=True
                                        )
                                        embedVar.remove_field(3)
                                    embedVar.title = dictItem["snippet"]["title"]
                                embedVar.description = dictItem["snippet"][
                                    "description"
                                ]
                                await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedValError = discord.Embed()
                        embedValError.description = (
                            "It seems like that search term didn't work.... 😭"
                        )
                        await ctx.respond(embed=embedValError)

                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = (
                        f"No results found for {search}. Please try again..."
                    )
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedError)

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
                searchDataMain = parser.parse(search_data, recursive=True)
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
                            dataMain3 = parser.parse(data, recursive=True)
                            print(dataMain3)
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
                                }
                                snippetFilter = [
                                    "title",
                                    "description",
                                    "thumbnails",
                                    "localized",
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
        """Returns up to 5 YouTube playlists based on the given YT channel"""
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
                searchDataMain = parser.parse(search_data, recursive=True)
                try:
                    if len(searchDataMain["items"]) == 0:
                        raise NoItemsError
                    else:
                        channel_id = searchDataMain["items"][0]["id"]["channelId"]
                        main_params = {
                            "key": YouTube_API_Key,
                            "part": "snippet,contentDetails",
                            "channelId": channel_id,
                            "maxResults": 3,
                        }
                        async with session.get(
                            "https://www.googleapis.com/youtube/v3/playlists",
                            params=main_params,
                        ) as r2:
                            data = await r2.content.read()
                            dataMain = parser.parse(data, recursive=True)
                            try:
                                embedVar = discord.Embed(
                                    color=discord.Color.from_rgb(255, 224, 224)
                                )
                                filterList = [
                                    "localized",
                                    "kind",
                                    "etag",
                                    "contentDetails",
                                    "snippet",
                                    "id",
                                ]
                                snippetList = [
                                    "thumbnails",
                                    "localized",
                                    "title",
                                    "description",
                                ]
                                videoFilter = ["default", "medium", "high", "standard"]
                                if len(dataMain["items"]) == 0:
                                    raise ValueError
                                else:
                                    for dictItems in dataMain["items"]:
                                        for k, v in dictItems.items():
                                            if k not in filterList:
                                                embedVar.add_field(
                                                    name=k, value=v, inline=True
                                                )
                                                embedVar.remove_field(3)

                                        for keys, val in dictItems["snippet"].items():
                                            if keys not in snippetList:
                                                embedVar.add_field(
                                                    name=keys, value=val, inline=True
                                                )
                                                embedVar.remove_field(3)

                                        for item, res in dictItems["snippet"][
                                            "thumbnails"
                                        ].items():
                                            if item not in videoFilter:
                                                embedVar.set_image(url=res["url"])

                                        embedVar.title = dictItems["snippet"]["title"]
                                        embedVar.description = dictItems["snippet"][
                                            "description"
                                        ]

                                        await ctx.respond(embed=embedVar)

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

    @yt.command(name="comments")
    async def youtube_comments(self, ctx, *, vid_id: Option(str, "YT Video ID")):
        """Returns up to 5 comments for the given YouTube video"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": YouTube_API_Key,
                "part": "snippet",
                "videoId": vid_id,
                "textFormat": "plainText",
                "maxResults": 5,
            }
            async with session.get(
                "https://www.googleapis.com/youtube/v3/commentThreads", params=params
            ) as r:
                data = await r.content.read()
                dataMain4 = parser.parse(data, recursive=True)
                try:
                    try:
                        if r.status == 403:
                            embedVar = discord.Embed()
                            embedVar.description = "Sadly this video or channel has disabled comments, thus no comments can be show. Please try again..."
                            embedVar.add_field(
                                name="Error",
                                value=dataMain4["error"]["message"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Reason",
                                value=dataMain4["error"]["errors"][0]["reason"],
                                inline=True,
                            )
                            await ctx.respond(embed=embedVar)
                        else:
                            embedVar = discord.Embed(
                                color=discord.Color.from_rgb(255, 125, 125)
                            )
                            snippetFilter = ["topLevelComment", "videoId"]
                            topLevelCommentFilter = [
                                "authorChannelId",
                                "authorProfileImageUrl",
                                "textOriginal",
                                "textDisplay",
                                "videoId",
                                "authorDisplayName",
                                "viewerRating",
                                "canRate",
                                "id",
                                "authorChannelUrl",
                                "videoId",
                            ]
                            pfpFilter = [
                                "videoId",
                                "textDisplay",
                                "textOriginal",
                                "authorDisplayName",
                                "authorChannelId",
                                "canRate",
                                "viewerRating",
                                "likeCount",
                                "publishedAt",
                                "updatedAt",
                                "authorChannelUrl",
                            ]
                            if len(dataMain4["items"]) == 0:
                                raise ValueError
                            elif "items" in dataMain4:
                                raise KeyError
                            else:
                                for dictVal in dataMain4["items"]:
                                    embedVar.title = dictVal["snippet"][
                                        "topLevelComment"
                                    ]["snippet"]["authorDisplayName"]
                                    embedVar.description = dictVal["snippet"][
                                        "topLevelComment"
                                    ]["snippet"]["textDisplay"]

                                    for k, v in dictVal["snippet"].items():
                                        if k not in snippetFilter:
                                            embedVar.add_field(
                                                name=k, value=v, inline=True
                                            )
                                            embedVar.remove_field(6)

                                    for key, res in dictVal["snippet"][
                                        "topLevelComment"
                                    ]["snippet"].items():
                                        if key not in topLevelCommentFilter:
                                            embedVar.add_field(
                                                name=key, value=res, inline=True
                                            )
                                            embedVar.remove_field(6)

                                    for item, img in dictVal["snippet"][
                                        "topLevelComment"
                                    ]["snippet"].items():
                                        if item not in pfpFilter:
                                            embedVar.set_thumbnail(url=img)

                                    await ctx.respond(embed=embedVar)
                    except KeyError:
                        embedError = discord.Embed()
                        embedError.description = (
                            "Sorry, it seems like the video can't be found..."
                        )
                        await ctx.respond(embed=embedError)
                except ValueError:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sorry, it seems like this channel doesn't exist..."
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @yt.command(name="video")
    async def youtube_video(self, ctx, *, video_id: Option(str, "YT Video ID")):
        """Returns some info on the given YouTube video"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "key": YouTube_API_Key,
                "part": "snippet,status,statistics",
                "id": video_id,
                "maxResults": 1,
            }
            async with session.get(
                "https://www.googleapis.com/youtube/v3/videos", params=params
            ) as another_response:
                data = await another_response.content.read()
                dataMain5 = parser.parse(data, recursive=True)
                try:

                    embed = discord.Embed(color=discord.Color.from_rgb(255, 0, 0))
                    snippetFilter = ["title", "description", "thumbnails", "localized"]
                    picFilter = ["default", "medium", "high", "standard"]
                    if len(dataMain5["items"]) == 0:
                        raise ValueError
                    else:
                        for items in dataMain5["items"]:
                            for keys, val in items["snippet"].items():
                                if keys not in snippetFilter:
                                    embed.add_field(name=keys, value=val, inline=True)
                            embed.title = items["snippet"]["title"]
                            embed.description = items["snippet"]["description"]
                            for key, value in items["statistics"].items():
                                embed.add_field(name=key, value=value, inline=True)
                            for k, v in items["snippet"]["thumbnails"].items():
                                if k not in picFilter:
                                    embed.set_image(url=v["url"])
                        await ctx.respond(embed=embed)
                except ValueError:
                    embedError = discord.Embed()
                    embedError.description = "Sorry, it seems like there wasn't any results... Please try again"
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(YoutubeV1(bot))
