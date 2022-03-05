import asyncio
import os

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands
from discord.commands import slash_command, Option
from dotenv import load_dotenv
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

Password = os.getenv("Postgres_Password")
Server_IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")


class tokenFetcher:
    def __init__(self):
        self.self = self

    async def get(self):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:5432/rin-deviantart-tokens"
        )
        tokens = Table(
            "DA_Tokens",
            meta,
            Column("Access_Tokens", String),
            Column("Refresh_Tokens", String),
        )
        async with engine.connect() as conn:
            s = tokens.select()
            result_select = await conn.execute(s)
            for row in result_select:
                return row


class DeviantArtV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="deviantart-item", description="Returns info about a deviation on DeviantArt", guild_ids=[866199405090308116])
    async def da(self, ctx, *, deviation_id: Option(str, "The ID for the Deviation")):
        token = tokenFetcher()
        accessToken = await token.get()
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "with_session": "false",
                "limit": "5",
                "access_token": f"{accessToken[0]}",
            }
            async with session.get(
                f"https://www.deviantart.com/api/v1/oauth2/deviation/{deviation_id}",
                params=params,
            ) as r:
                deviation = await r.json()
                embedVar = discord.Embed(color=discord.Color.from_rgb(255, 214, 214))
                try:
                    if r.status == 200:
                        filter = ["author", "stats", "preview", "thumbs", "content", "title", "printid", "download_filesize"]
                        authorFilterMain = ["type", "is_subscribed", "usericon"]
                        for keys, values in deviation.items():
                            if keys not in filter:
                                embedVar.add_field(name=keys, value=values, inline=True)
                        for k, v in deviation["author"].items():
                            if k not in authorFilterMain:
                                embedVar.add_field(name=k, value=v, inline=True)
                        for item, res in deviation["stats"].items():
                            embedVar.add_field(name=item, value=res, inline=True)
                        embedVar.title = deviation["title"]
                        embedVar.set_image(url=deviation["content"]["src"])
                        embedVar.set_thumbnail(url=deviation["author"]["usericon"])
                        await ctx.respond(embed=embedVar)
                    else:
                        embedVar = discord.Embed(
                            color=discord.Color.from_rgb(255, 214, 214)
                        )
                        embedVar.description = "The query failed. Please try again"
                        embedVar.add_field(
                            name="Error", value=deviation["error"], inline=True
                        )
                        embedVar.add_field(
                            name="Error Description",
                            value=deviation["error_description"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Status", value=deviation["status"], inline=True
                        )
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(name="Reason", value=e, inline=False)
                    embedVar.add_field(
                        name="Error", value=deviation["error"], inline=True
                    )
                    embedVar.add_field(
                        name="Error Description",
                        value=deviation["error_description"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Status", value=deviation["status"], inline=True
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DeviantArtV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="deviantart-newest", description="Returns up to 5 newest art from DeviantArt based on the given search result", guild_ids=[866199405090308116])
    async def da_query(self, ctx, *, search_newest: Option(str, "The search term you want to use to fetch the latest art")):
        token = tokenFetcher()
        search_newest = search_newest.replace(" ", "%20")
        accessToken = await token.get()
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": f"{search_newest}",
                "with_session": "false",
                "limit": 5,
                "mature_content": "False",
                "access_token": f"{accessToken[0]}",
            }
            async with session.get(
                "https://www.deviantart.com/api/v1/oauth2/browse/newest", params=params
            ) as resp:
                art = await resp.json()
                embedVar = discord.Embed(color=discord.Color.from_rgb(255, 156, 192))
                try:
                    artFilter = ["preview", "content", "author", "thumbs", "title", "stats", "printid", "is_deleted", "is_favourited", "download_filesize", "category_path"]
                    authorFilter = ["type", "is_subscribed", "usericon"]
                    for dictItem in art["results"]:
                        for k, v in dictItem["author"].items():
                            if k not in authorFilter:
                                embedVar.add_field(name=k, value=v, inline=True)
                                embedVar.remove_field(-11)
                        for key, value in dictItem.items():
                            if key not in artFilter:
                                embedVar.add_field(name=key, value=value, inline=True)
                                embedVar.remove_field(-11)
                        embedVar.title = dictItem["title"]
                        embedVar.set_image(url=dictItem["content"]["src"])
                        embedVar.set_thumbnail(url=dictItem["author"]["usericon"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(name="Reason", value=e, inline=False)
                    embedVar.add_field(
                        name="Error", value=art["error"], inline=True)
                    embedVar.add_field(
                        name="Error Description",
                        value=art["error_description"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Status", value=art["status"], inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DeviantArtV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="deviantart-popular", description="Returns up to 5 popular art from DeviantArt based on the given search result", guild_ids=[866199405090308116])
    async def deviantart_popular(self, ctx, *, search_popular: Option(str, "The search term you want to use to fetch the popular art")):
        token = tokenFetcher()
        accessToken = await token.get()
        search_popular = search_popular.replace(" ", "%20")
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": f"{search_popular}",
                "with_session": "false",
                "limit": "5",
                "mature_content": "false",
                "access_token": f"{accessToken[0]}",
            }
            async with session.get(
                "https://www.deviantart.com/api/v1/oauth2/browse/popular", params=params
            ) as response:
                pop = await response.json()
                embedVar = discord.Embed(color=discord.Color.from_rgb(255, 250, 181))
                try:
                    artFilter = ["preview", "content", "author", "thumbs", "title", "stats",
                                 "is_deleted", "is_favourited", "download_filesize", "category_path"]
                    authorFilter = ["type", "is_subscribed", "usericon"]
                    for dictItem2 in pop["results"]:
                        for k, v in dictItem2["author"].items():
                            if k not in authorFilter:
                                embedVar.add_field(name=k, value=v, inline=True)
                                embedVar.remove_field(-13)
                        for key, value in dictItem2.items():
                            if key not in artFilter:
                                embedVar.add_field(name=key, value=value, inline=True)
                                embedVar.remove_field(-13)
                        for item3, res3 in dictItem2["stats"].items():
                            embedVar.add_field(name=item3, value=res3, inline=True)
                            embedVar.remove_field(-13)
                        embedVar.title = dictItem2["title"]
                        embedVar.set_image(url=dictItem2["content"]["src"])
                        embedVar.set_thumbnail(url=dictItem2["author"]["usericon"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(name="Reason", value=e, inline=False)
                    embedVar.add_field(
                        name="Error", value=pop["error"], inline=True)
                    embedVar.add_field(
                        name="Error Description",
                        value=pop["error_description"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Status", value=pop["status"], inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

class DeviantArtV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="deviantart-tag-search", description="Returns up to 5 search results from DeviantArt based on the given tag", guild_ids=[866199405090308116])
    async def tags(self, ctx, *, tag: Option(str, "The tag you want to use to fetch the search results")):
        token = tokenFetcher()
        accessToken = await token.get()
        tag = tag.replace(" ", "%20")
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "tag": f"{tag}",
                "with_session": "false",
                "limit": "5",
                "mature_content": "false",
                "access_token": f"{accessToken[0]}",
            }
            async with session.get(
                "https://www.deviantart.com/api/v1/oauth2/browse/tags", params=params
            ) as rep:
                tags = await rep.json()
                embedVar = discord.Embed(color=discord.Color.from_rgb(235, 186, 255))
                try:
                    tagsFilter = ["preview", "content", "author", "thumbs", "title", "stats",
                                  "is_deleted", "is_favourited", "download_filesize", "category_path"]
                    authorFilter3 = ["type", "is_subscribed", "usericon"]
                    for dictItem3 in tags["results"]:
                        for k, v in dictItem3["author"].items():
                            if k not in authorFilter3:
                                embedVar.add_field(name=k, value=v, inline=True)
                                embedVar.remove_field(-13)
                        for key, value in dictItem3.items():
                            if key not in tagsFilter:
                                embedVar.add_field(name=key, value=value, inline=True)
                                embedVar.remove_field(-13)
                        for item3, res3 in dictItem3["stats"].items():
                            embedVar.add_field(name=item3, value=res3, inline=True)
                            embedVar.remove_field(-13)
                        embedVar.title = dictItem3["title"]
                        embedVar.set_image(url=dictItem3["content"]["src"])
                        embedVar.set_thumbnail(url=dictItem3["author"]["usericon"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(name="Reason", value=e, inline=False)
                    embedVar.add_field(
                        name="Error", value=tags["error"], inline=True)
                    embedVar.add_field(
                        name="Error Description",
                        value=tags["error_description"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Status", value=tags["status"], inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())



class DeviantArtV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="deviantart-user", description="Returns the user's profile information", guild_ids=[866199405090308116])
    async def userv1(self, ctx, *, user: Option(str, "The username you want to search for")):
        token = tokenFetcher()
        accessToken = await token.get()
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "ext_collections": "false",
                "ext_galleries": "false",
                "with_session": "false",
                "mature_content": "false",
                "access_token": f"{accessToken[0]}",
            }
            async with session.get(
                f"https://www.deviantart.com/api/v1/oauth2/user/profile/{user}",
                params=params,
            ) as respon:
                users = await respon.json()
                usersFilter = ["bio", "tagline", "cover_deviation", "last_status", "cover_photo", "stats", "user"]
                embedVar = discord.Embed()
                try:
                    if "cover_deviation" in users:
                        for keys, value in users.items():
                            if keys not in usersFilter:
                                embedVar.add_field(name=keys, value=f"[{value}]", inline=True)
                        for k, v in users["stats"].items():
                            embedVar.add_field(name=k, value=f"[{v}]", inline=True)
                        embedVar.title = users["user"]["username"]
                        embedVar.description = f"{users['tagline']}\n\n{users['bio']}"
                        embedVar.set_thumbnail(url=users["user"]["usericon"])
                        embedVar.set_image(url=users["cover_deviation"]["cover_deviation"]["content"]["src"])
                        await ctx.respond(embed=embedVar)
                    else:
                        for keys1, value1 in users.items():
                            if keys1 not in usersFilter:
                                embedVar.add_field(name=keys1, value=f"[{value1}]", inline=True)
                        for k1, v1 in users["stats"].items():
                            embedVar.add_field(name=k1, value=f"[{v1}]", inline=True)
                        embedVar.title = users["user"]["username"]
                        embedVar.description = f"{users['tagline']}\n\n{users['bio']}"
                        embedVar.set_thumbnail(url=users["user"]["usericon"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(name="Reason", value=e, inline=False)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(DeviantArtV1(bot))
    bot.add_cog(DeviantArtV2(bot))
    bot.add_cog(DeviantArtV3(bot))
    bot.add_cog(DeviantArtV4(bot))
    bot.add_cog(DeviantArtV5(bot))
