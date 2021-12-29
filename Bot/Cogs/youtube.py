import os

import aiohttp
import discord
import orjson
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

YouTube_API_Key = os.getenv("YouTube_API_Key")


class YoutubeV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="youtube-search", aliases=["yt-search"])
    async def youtube_search(self, ctx, *, search: str):
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
                data = await r.json()
                try:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(212, 255, 223)
                    )
                    embedVar.title = data["items"][0]["snippet"]["title"]
                    embedVar.add_field(
                        name="Channel Title",
                        value=data["items"][0]["snippet"]["channelTitle"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Channel ID",
                        value=data["items"][0]["snippet"]["channelId"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Published Time",
                        value=data["items"][0]["snippet"]["publishedAt"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Video ID",
                        value=data["items"][0]["id"]["videoId"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Youtube Link",
                        value=f"https://www.youtube.com/watch?v={data['items'][0]['id']['videoId']}",
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Youtube Channel Link",
                        value=f"https://www.youtube.com/channel/{data['items'][0]['snippet']['channelId']}",
                        inline=True,
                    )
                    embedVar.description = data["items"][0]["snippet"]["description"]
                    embedVar.set_image(
                        url=data["items"][0]["snippet"]["thumbnails"]["high"]["url"]
                    )
                    await ctx.send(embed=embedVar)
                    embedVar2 = discord.Embed(
                        color=discord.Color.from_rgb(212, 238, 255)
                    )
                    embedVar2.title = data["items"][1]["snippet"]["title"]
                    embedVar2.add_field(
                        name="Channel Title",
                        value=data["items"][1]["snippet"]["channelTitle"],
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Channel ID",
                        value=data["items"][1]["snippet"]["channelId"],
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Published Time",
                        value=data["items"][1]["snippet"]["publishedAt"],
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Video ID",
                        value=data["items"][1]["id"]["videoId"],
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Youtube Link",
                        value=f"https://www.youtube.com/watch?v={data['items'][1]['id']['videoId']}",
                        inline=True,
                    )
                    embedVar2.add_field(
                        name="Youtube Channel Link",
                        value=f"https://www.youtube.com/channel/{data['items'][1]['snippet']['channelId']}",
                        inline=True,
                    )
                    embedVar2.description = data["items"][1]["snippet"]["description"]
                    embedVar2.set_image(
                        url=data["items"][1]["snippet"]["thumbnails"]["high"]["url"]
                    )
                    await ctx.send(embed=embedVar2)
                    embedVar3 = discord.Embed(
                        color=discord.Color.from_rgb(223, 212, 255)
                    )
                    embedVar3.title = data["items"][2]["snippet"]["title"]
                    embedVar3.add_field(
                        name="Channel Title",
                        value=data["items"][2]["snippet"]["channelTitle"],
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Channel ID",
                        value=data["items"][2]["snippet"]["channelId"],
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Published Time",
                        value=data["items"][2]["snippet"]["publishedAt"],
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Video ID",
                        value=data["items"][2]["id"]["videoId"],
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Youtube Link",
                        value=f"https://www.youtube.com/watch?v={data['items'][2]['id']['videoId']}",
                        inline=True,
                    )
                    embedVar3.add_field(
                        name="Youtube Channel Link",
                        value=f"https://www.youtube.com/channel/{data['items'][2]['snippet']['channelId']}",
                        inline=True,
                    )
                    embedVar3.description = data["items"][2]["snippet"]["description"]
                    embedVar3.set_image(
                        url=data["items"][2]["snippet"]["thumbnails"]["high"]["url"]
                    )
                    await ctx.send(embed=embedVar3)
                    embedVar4 = discord.Embed(
                        color=discord.Color.from_rgb(255, 212, 253)
                    )
                    embedVar4.title = data["items"][3]["snippet"]["title"]
                    embedVar4.add_field(
                        name="Channel Title",
                        value=data["items"][3]["snippet"]["channelTitle"],
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Channel ID",
                        value=data["items"][3]["snippet"]["channelId"],
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Published Time",
                        value=data["items"][3]["snippet"]["publishedAt"],
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Video ID",
                        value=data["items"][3]["id"]["videoId"],
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Youtube Link",
                        value=f"https://www.youtube.com/watch?v={data['items'][3]['id']['videoId']}",
                        inline=True,
                    )
                    embedVar4.add_field(
                        name="Youtube Channel Link",
                        value=f"https://www.youtube.com/channel/{data['items'][3]['snippet']['channelId']}",
                        inline=True,
                    )
                    embedVar4.description = data["items"][3]["snippet"]["description"]
                    embedVar4.set_image(
                        url=data["items"][3]["snippet"]["thumbnails"]["high"]["url"]
                    )
                    await ctx.send(embed=embedVar4)
                    embedVar5 = discord.Embed(
                        color=discord.Color.from_rgb(255, 212, 212)
                    )
                    embedVar5.title = data["items"][4]["snippet"]["title"]
                    embedVar5.add_field(
                        name="Channel Title",
                        value=data["items"][4]["snippet"]["channelTitle"],
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Channel ID",
                        value=data["items"][4]["snippet"]["channelId"],
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Published Time",
                        value=data["items"][4]["snippet"]["publishedAt"],
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Video ID",
                        value=data["items"][4]["id"]["videoId"],
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Youtube Link",
                        value=f"https://www.youtube.com/watch?v={data['items'][4]['id']['videoId']}",
                        inline=True,
                    )
                    embedVar5.add_field(
                        name="Youtube Channel Link",
                        value=f"https://www.youtube.com/channel/{data['items'][4]['snippet']['channelId']}",
                        inline=True,
                    )
                    embedVar5.description = data["items"][4]["snippet"]["description"]
                    embedVar5.set_image(
                        url=data["items"][4]["snippet"]["thumbnails"]["high"]["url"]
                    )
                    await ctx.send(embed=embedVar5)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = (
                        f"No results found for {search}. Please try again..."
                    )
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.send(embed=embedError)

    @youtube_search.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class YoutubeV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="youtube-channel", aliases=["yt-channel"])
    async def youtube_channel(self, ctx, *, search: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            search_params = {
                "key": YouTube_API_Key,
                "part": "snippet",
                "type": "channel",
                "maxResults": "1",
                "q": search,
                "channelType": "any",
                "videoLicense": "any",
                "order": "relevance",
            }
            async with session.get(
                "https://www.googleapis.com/youtube/v3/search", params=search_params
            ) as response:
                search_data = await response.json()
                channel_id = search_data["items"][0]["id"]["channelId"]
                params = {
                    "key": YouTube_API_Key,
                    "part": "snippet,statistics",
                    "id": channel_id,
                }
                async with session.get(
                    "https://www.googleapis.com/youtube/v3/channels", params=params
                ) as re:
                    data = await re.json()
                    try:
                        embedVar = discord.Embed(
                            color=discord.Color.from_rgb(255, 0, 0)
                        )
                        embedVar.title = data["items"][0]["snippet"]["title"]
                        embedVar.add_field(
                            name="View Count",
                            value=data["items"][0]["statistics"]["viewCount"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Subscriber Count",
                            value=data["items"][0]["statistics"]["subscriberCount"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Video Count",
                            value=data["items"][0]["statistics"]["videoCount"],
                            inline=True,
                        )
                        embedVar.description = data["items"][0]["snippet"][
                            "description"
                        ]
                        embedVar.set_thumbnail(
                            url=data["items"][0]["snippet"]["thumbnails"]["high"]["url"]
                        )
                        await ctx.send(embed=embedVar)
                    except Exception as e:
                        embedError = discord.Embed()
                        embedError.description = (
                            f"No results found for {search}. Please try again..."
                        )
                        embedError.add_field(
                            name="Error", value=e, inline=True)
                        await ctx.send(embed=embedError)

    @youtube_channel.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class YoutubeV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="youtube-playlists", aliases=["yt-playlists"])
    async def youtube_playlists(self, ctx, *, search: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            search_params = {
                "key": YouTube_API_Key,
                "part": "snippet",
                "type": "playlists",
                "maxResults": "1",
                "q": search,
            }
            async with session.get(
                "https://www.googleapis.com/youtube/v3/search", params=search_params
            ) as response2:
                search_data = await response2.json()
                channel_id = search_data["items"][0]["id"]["channelId"]
                main_params = {
                    "key": YouTube_API_Key,
                    "part": "snippet,contentDetails",
                    "channelId": channel_id,
                    "maxResults": 5,
                }
                async with session.get(
                    "https://www.googleapis.com/youtube/v3/playlists",
                    params=main_params,
                ) as r2:
                    data = await r2.json()
                    try:
                        embedVar1 = discord.Embed(
                            color=discord.Color.from_rgb(255, 224, 224)
                        )
                        embedVar1.title = data["items"][0]["snippet"]["title"]
                        embedVar1.description = data["items"][0]["snippet"]["description"]
                        embedVar1.add_field(
                            name="Channel",
                            value=data["items"][0]["snippet"]["channelTitle"],
                            inline=True,
                        )
                        embedVar1.add_field(
                            name="Amount of Videos in Playlist",
                            value=data["items"][0]["contentDetails"]["itemCount"],
                            inline=True,
                        )
                        embedVar1.set_image(
                            url=data["items"][0]["snippet"]["thumbnails"]["maxres"]["url"]
                        )
                        await ctx.send(embed=embedVar1)
                        embedVar2 = discord.Embed(
                            color=discord.Color.from_rgb(249, 255, 224)
                        )
                        embedVar2.title = data["items"][1]["snippet"]["title"]
                        embedVar2.description = data["items"][1]["snippet"]["description"]
                        embedVar2.add_field(
                            name="Channel",
                            value=data["items"][1]["snippet"]["channelTitle"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Amount of Videos in Playlist",
                            value=data["items"][1]["contentDetails"]["itemCount"],
                            inline=True,
                        )
                        embedVar2.set_image(
                            url=data["items"][1]["snippet"]["thumbnails"]["maxres"]["url"]
                        )
                        await ctx.send(embed=embedVar2)
                        embedVar3 = discord.Embed(
                            color=discord.Color.from_rgb(224, 255, 228)
                        )
                        embedVar3.title = data["items"][2]["snippet"]["title"]
                        embedVar3.description = data["items"][2]["snippet"]["description"]
                        embedVar3.add_field(
                            name="Channel",
                            value=data["items"][2]["snippet"]["channelTitle"],
                            inline=True,
                        )
                        embedVar3.add_field(
                            name="Amount of Videos in Playlist",
                            value=data["items"][2]["contentDetails"]["itemCount"],
                            inline=True,
                        )
                        embedVar3.set_image(
                            url=data["items"][2]["snippet"]["thumbnails"]["maxres"]["url"]
                        )
                        await ctx.send(embed=embedVar3)
                        embedVar4 = discord.Embed(
                            color=discord.Color.from_rgb(224, 240, 255)
                        )
                        embedVar4.title = data["items"][3]["snippet"]["title"]
                        embedVar4.description = data["items"][3]["snippet"]["description"]
                        embedVar4.add_field(
                            name="Channel",
                            value=data["items"][3]["snippet"]["channelTitle"],
                            inline=True,
                        )
                        embedVar4.add_field(
                            name="Amount of Videos in Playlist",
                            value=data["items"][3]["contentDetails"]["itemCount"],
                            inline=True,
                        )
                        embedVar4.set_image(
                            url=data["items"][3]["snippet"]["thumbnails"]["maxres"]["url"]
                        )
                        await ctx.send(embed=embedVar4)
                        embedVar5 = discord.Embed(
                            color=discord.Color.from_rgb(242, 224, 255)
                        )
                        embedVar5.title = data["items"][4]["snippet"]["title"]
                        embedVar5.description = data["items"][4]["snippet"]["description"]
                        embedVar5.add_field(
                            name="Channel",
                            value=data["items"][4]["snippet"]["channelTitle"],
                            inline=True,
                        )
                        embedVar5.add_field(
                            name="Amount of Videos in Playlist",
                            value=data["items"][4]["contentDetails"]["itemCount"],
                            inline=True,
                        )
                        embedVar5.set_image(
                            url=data["items"][4]["snippet"]["thumbnails"]["maxres"]["url"]
                        )
                        await ctx.send(embed=embedVar5)
                    except Exception as e:
                        embedError = discord.Embed()
                        embedError.description = (
                            f"No results found for {search}. Please try again..."
                        )
                        embedError.add_field(
                            name="Error", value=e, inline=True)
                        await ctx.send(embed=embedError)
                        
    @youtube_playlists.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

class YoutubeV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="youtube-comments", aliases=["yt-comments"])
    async def youtube_comments(self, ctx, *, id:str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": YouTube_API_Key, "part": "snippet", "videoId": id, "textFormat": "plainText", "maxResults": 5}
            async with session.get("https://www.googleapis.com/youtube/v3/commentThreads", params=params) as r:
                data = await r.json()
                try:
                    if r.status == 403:
                        embedVar = discord.Embed()
                        embedVar.description = "Sadly this video or channel has disabled comments, thus no comments can be show. Please try again..."
                        embedVar.add_field(name="Error", value=data["error"]["message"], inline=True)
                        embedVar.add_field(name="Reason", value=data["error"]["errors"][0]["reason"], inline=True)
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar1 = discord.Embed(color=discord.Color.from_rgb(255, 125, 125))
                        embedVar1.title = data["items"][0]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                        embedVar1.description = data["items"][0]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                        embedVar1.add_field(name="Like Count", value=data["items"][0]["snippet"]["topLevelComment"]["snippet"]["likeCount"], inline=True)
                        embedVar1.add_field(name="Published Date", value=data["items"][0]["snippet"]["topLevelComment"]["snippet"]["publishedAt"], inline=True)
                        embedVar1.add_field(name="Updated Date", value=data["items"][0]["snippet"]["topLevelComment"]["snippet"]["updatedAt"], inline=True)
                        embedVar1.set_thumbnail(url=data["items"][0]["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"])
                        await ctx.send(embed=embedVar1)
                        embedVar2 = discord.Embed(color=discord.Color.from_rgb(255, 253, 125))
                        embedVar2.title = data["items"][1]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                        embedVar2.description = data["items"][1]["snippet"]["topLevelComment"]["snippet"][
                            "textOriginal"]
                        embedVar2.add_field(name="Like Count",
                                            value=data["items"][1]["snippet"]["topLevelComment"]["snippet"][
                                                "likeCount"], inline=True)
                        embedVar2.add_field(name="Published Date",
                                            value=data["items"][1]["snippet"]["topLevelComment"]["snippet"][
                                                "publishedAt"], inline=True)
                        embedVar2.add_field(name="Updated Date",
                                            value=data["items"][1]["snippet"]["topLevelComment"]["snippet"][
                                                "updatedAt"], inline=True)
                        embedVar2.set_thumbnail(
                            url=data["items"][1]["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"])
                        await ctx.send(embed=embedVar2)
                        embedVar3 = discord.Embed(color=discord.Color.from_rgb(129, 255, 125))
                        embedVar3.title = data["items"][2]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                        embedVar3.description = data["items"][2]["snippet"]["topLevelComment"]["snippet"][
                            "textOriginal"]
                        embedVar3.add_field(name="Like Count",
                                            value=data["items"][2]["snippet"]["topLevelComment"]["snippet"][
                                                "likeCount"], inline=True)
                        embedVar3.add_field(name="Published Date",
                                            value=data["items"][2]["snippet"]["topLevelComment"]["snippet"][
                                                "publishedAt"], inline=True)
                        embedVar3.add_field(name="Updated Date",
                                            value=data["items"][2]["snippet"]["topLevelComment"]["snippet"][
                                                "updatedAt"], inline=True)
                        embedVar3.set_thumbnail(
                            url=data["items"][2]["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"])
                        await ctx.send(embed=embedVar3)
                        embedVar4 = discord.Embed(color=discord.Color.from_rgb(125, 255, 244))
                        embedVar4.title = data["items"][3]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                        embedVar4.description = data["items"][3]["snippet"]["topLevelComment"]["snippet"][
                            "textOriginal"]
                        embedVar4.add_field(name="Like Count",
                                            value=data["items"][3]["snippet"]["topLevelComment"]["snippet"][
                                                "likeCount"], inline=True)
                        embedVar4.add_field(name="Published Date",
                                            value=data["items"][3]["snippet"]["topLevelComment"]["snippet"][
                                                "publishedAt"], inline=True)
                        embedVar4.add_field(name="Updated Date",
                                            value=data["items"][3]["snippet"]["topLevelComment"]["snippet"][
                                                "updatedAt"], inline=True)
                        embedVar4.set_thumbnail(
                            url=data["items"][3]["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"])
                        await ctx.send(embed=embedVar4)
                        embedVar5 = discord.Embed(color=discord.Color.from_rgb(160, 125, 255))
                        embedVar5.title = data["items"][4]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                        embedVar5.description = data["items"][4]["snippet"]["topLevelComment"]["snippet"][
                            "textOriginal"]
                        embedVar5.add_field(name="Like Count",
                                            value=data["items"][4]["snippet"]["topLevelComment"]["snippet"][
                                                "likeCount"], inline=True)
                        embedVar5.add_field(name="Published Date",
                                            value=data["items"][4]["snippet"]["topLevelComment"]["snippet"][
                                                "publishedAt"], inline=True)
                        embedVar5.add_field(name="Updated Date",
                                            value=data["items"][4]["snippet"]["topLevelComment"]["snippet"][
                                                "updatedAt"], inline=True)
                        embedVar5.set_thumbnail(
                            url=data["items"][4]["snippet"]["topLevelComment"]["snippet"]["authorProfileImageUrl"])
                        await ctx.send(embed=embedVar5)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Sorry, there seemed to be an error. Please try again..."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.send(embed=embedError)
                    
    @youtube_comments.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
            
class YoutubeV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="youtube-video", aliases=["yt-video"])
    async def youtube_video(self, ctx, *, id:str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": YouTube_API_Key, "part": "snippet,status,statistics", "id": id, "maxResults": 1}
            async with session.get("https://www.googleapis.com/youtube/v3/videos", params=params) as another_response:
                data = await another_response.json()
                try:
                    embed = discord.Embed(color=discord.Color.from_rgb(255, 0, 0))
                    embed.title = data["items"][0]["snippet"]["title"]
                    embed.description = data["items"][0]["snippet"]["description"]
                    embed.add_field(name="Channel", value=data["items"][0]["snippet"]["channelTitle"], inline=True)
                    embed.add_field(name="Views", value=data["items"][0]["statistics"]["viewCount"], inline=True)
                    embed.add_field(name="Likes", value=data["items"][0]["statistics"]["likeCount"], inline=True)
                    embed.add_field(name="Comments", value=data["items"][0]["statistics"]["commentCount"], inline=True)
                    embed.add_field(name="Favorite Count", value=data["items"][0]["statistics"]["favoriteCount"], inline=True)
                    embed.set_image(url=data["items"][0]["snippet"]["thumbnails"]["maxres"]["url"])
                    await ctx.send(embed=embed)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = "Sorry, there seemed to be an error. Please try again..."
                    embedError.add_field(name="Error", value=e, inline=True)
                    await ctx.send(embed=embedError)
def setup(bot):
    bot.add_cog(YoutubeV1(bot))
    bot.add_cog(YoutubeV2(bot))
    bot.add_cog(YoutubeV3(bot))
    bot.add_cog(YoutubeV4(bot))
    bot.add_cog(YoutubeV5(bot))
