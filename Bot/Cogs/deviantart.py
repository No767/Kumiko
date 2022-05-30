import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from exceptions import NoItemsError
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

Password = os.getenv("Postgres_Password")
Server_IP = os.getenv("Postgres_Server_IP")
Username = os.getenv("Postgres_Username")
Port = os.getenv("Postgres_Port")
Database = os.getenv("Postgres_Database")

parser = simdjson.Parser()


class tokenFetcher:
    def __init__(self):
        self.self = self

    async def get(self):
        meta = MetaData()
        engine = create_async_engine(
            f"postgresql+asyncpg://{Username}:{Password}@{Server_IP}:{Port}/{Database}"
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

    da = SlashCommandGroup("deviantart", "Commands for DeviantArt")

    @da.command(name="item")
    async def daItem(
        self, ctx, *, deviation_id: Option(str, "The ID for the Deviation")
    ):
        """Returns info about a deviation on DeviantArt"""
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
                deviation = await r.content.read()
                deviationMain = parser.parse(deviation, recursive=True)
                embedVar = discord.Embed(color=discord.Color.from_rgb(255, 214, 214))
                try:
                    if r.status == 200:
                        filterItem = [
                            "author",
                            "stats",
                            "preview",
                            "thumbs",
                            "content",
                            "title",
                            "printid",
                            "download_filesize",
                        ]
                        authorFilterMain = ["type", "is_subscribed", "usericon"]
                        for keys, values in deviationMain.items():
                            if keys not in filterItem:
                                embedVar.add_field(name=keys, value=values, inline=True)
                        for k, v in deviationMain["author"].items():
                            if k not in authorFilterMain:
                                embedVar.add_field(name=k, value=v, inline=True)
                        for item, res in deviationMain["stats"].items():
                            embedVar.add_field(name=item, value=res, inline=True)
                        embedVar.title = deviationMain["title"]
                        embedVar.set_image(url=deviationMain["content"]["src"])
                        embedVar.set_thumbnail(url=deviationMain["author"]["usericon"])
                        await ctx.respond(embed=embedVar)
                    else:
                        embedVar = discord.Embed(
                            color=discord.Color.from_rgb(255, 214, 214)
                        )
                        embedVar.description = "It seems like either the data was put in incorrectly, or there is an issue. Please double check that the data is correct"
                        embedVar.add_field(
                            name="Error", value=deviationMain["error"], inline=True
                        )
                        embedVar.add_field(
                            name="Error Description",
                            value=deviationMain["error_description"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Status", value=deviationMain["status"], inline=True
                        )
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(name="Reason", value=e, inline=False)
                    embedVar.add_field(
                        name="Error", value=deviationMain["error"], inline=True
                    )
                    embedVar.add_field(
                        name="Error Description",
                        value=deviationMain["error_description"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Status", value=deviationMain["status"], inline=True
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @da.command(name="newest")
    async def da_query(
        self,
        ctx,
        *,
        search_newest: Option(
            str, "The search term you want to use to fetch the latest art"
        ),
    ):
        """Returns up to 50 newest art from DeviantArt based on the given search result"""
        token = tokenFetcher()
        search_newest = search_newest.replace(" ", "%20")
        accessToken = await token.get()
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": f"{search_newest}",
                "with_session": "false",
                "limit": 50,
                "mature_content": "False",
                "access_token": f"{accessToken[0]}",
            }
            async with session.get(
                "https://www.deviantart.com/api/v1/oauth2/browse/newest", params=params
            ) as resp:
                art = await resp.content.read()
                artMain = parser.parse(art, recursive=True)
                try:
                    try:
                        if len(artMain["results"]) == 0:
                            raise NoItemsError
                        else:
                            mainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        color=discord.Color.from_rgb(255, 156, 192),
                                        title=dictItem["title"],
                                    )
                                    .set_thumbnail(url=dictItem["author"]["usericon"])
                                    .set_image(url=dictItem["content"]["src"])
                                    .add_field(
                                        name="Author",
                                        value=dictItem["author"]["username"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Category",
                                        value=dictItem["category"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Comments",
                                        value=dictItem["stats"]["comments"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Favorites",
                                        value=dictItem["stats"]["favourites"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Downloadable",
                                        value=dictItem["is_downloadable"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Deviantion ID",
                                        value=dictItem["deviationid"],
                                        inline=True,
                                    )
                                    for dictItem in artMain["results"]
                                ]
                            )
                            await mainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = "Sorry, but there seems to be no posts from the search query given. Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except Exception:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(
                        name="Error", value=artMain["error"], inline=True
                    )
                    embedVar.add_field(
                        name="Error Description",
                        value=artMain["error_description"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Status", value=artMain["status"], inline=True
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @da.command(name="popular")
    async def deviantart_popular(
        self,
        ctx,
        *,
        search_popular: Option(
            str, "The search term you want to use to fetch the popular art"
        ),
    ):
        """Returns up to 50 popular art from DeviantArt based on the given search result"""
        token = tokenFetcher()
        accessToken = await token.get()
        search_popular = search_popular.replace(" ", "%20")
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "q": f"{search_popular}",
                "with_session": "false",
                "limit": 50,
                "mature_content": "false",
                "access_token": f"{accessToken[0]}",
            }
            async with session.get(
                "https://www.deviantart.com/api/v1/oauth2/browse/popular", params=params
            ) as response:
                pop = await response.content.read()
                popMain = parser.parse(pop, recursive=True)
                try:
                    try:
                        if len(popMain["results"]) == 0:
                            raise NoItemsError
                        else:
                            popMainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        color=discord.Color.from_rgb(255, 250, 181),
                                        title=dictItem2["title"],
                                    )
                                    .set_image(url=dictItem2["content"]["src"])
                                    .set_thumbnail(url=dictItem2["author"]["usericon"])
                                    .add_field(
                                        name="Author",
                                        value=dictItem2["author"]["username"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Category",
                                        value=dictItem2["category"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Comments",
                                        value=dictItem2["stats"]["comments"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Favorites",
                                        value=dictItem2["stats"]["favourites"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Downloadable",
                                        value=dictItem2["is_downloadable"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Deviantion ID",
                                        value=dictItem2["deviationid"],
                                        inline=True,
                                    )
                                    for dictItem2 in popMain["results"]
                                ]
                            )
                            await popMainPages.respond(ctx.interaction, ephemeral=False)
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = "It seems like there were no posts found... Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except Exception:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(
                        name="Error", value=popMain["error"], inline=True
                    )
                    embedVar.add_field(
                        name="Error Description",
                        value=popMain["error_description"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Status", value=popMain["status"], inline=True
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @da.command(name="tags")
    async def tagsMain(
        self,
        ctx,
        *,
        tag: Option(str, "The tag you want to use to fetch the search results"),
    ):
        """Returns up to 50 search results from DeviantArt based on the given tag"""
        token = tokenFetcher()
        accessToken = await token.get()
        tag = tag.replace(" ", "%20")
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "tag": f"{tag}",
                "with_session": "false",
                "limit": 50,
                "mature_content": "false",
                "access_token": f"{accessToken[0]}",
            }
            async with session.get(
                "https://www.deviantart.com/api/v1/oauth2/browse/tags", params=params
            ) as rep:
                tags = await rep.content.read()
                tagsMain = parser.parse(tags, recursive=True)
                embedVar = discord.Embed(color=discord.Color.from_rgb(235, 186, 255))
                try:
                    try:
                        if len(tagsMain["results"]) == 0:
                            raise NoItemsError
                        else:
                            tagsMainPages = pages.Paginator(
                                pages=[
                                    discord.Embed(
                                        color=discord.Color.from_rgb(255, 250, 181),
                                        title=dictItem3["title"],
                                    )
                                    .set_image(url=dictItem3["content"]["src"])
                                    .set_thumbnail(url=dictItem3["author"]["usericon"])
                                    .add_field(
                                        name="Author",
                                        value=dictItem3["author"]["username"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Category",
                                        value=dictItem3["category"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Comments",
                                        value=dictItem3["stats"]["comments"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Favorites",
                                        value=dictItem3["stats"]["favourites"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Downloadable",
                                        value=dictItem3["is_downloadable"],
                                        inline=True,
                                    )
                                    .add_field(
                                        name="Deviantion ID",
                                        value=dictItem3["deviationid"],
                                        inline=True,
                                    )
                                    for dictItem3 in tagsMain["results"]
                                ]
                            )
                            await tagsMainPages.respond(
                                ctx.interaction, ephemeral=False
                            )
                    except NoItemsError:
                        embedNoItemsError = discord.Embed()
                        embedNoItemsError.description = "It seems like there were no posts found... Please try again"
                        await ctx.respond(embed=embedNoItemsError)
                except Exception:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedVar.description = "The query failed. Please try again"
                    embedVar.add_field(
                        name="Error", value=tagsMain["error"], inline=True
                    )
                    embedVar.add_field(
                        name="Error Description",
                        value=tagsMain["error_description"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Status", value=tagsMain["status"], inline=True
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @da.command(name="users")
    async def userv1(
        self, ctx, *, user: Option(str, "The username you want to search for")
    ):
        """Returns the user's profile information"""
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
                users = await respon.content.read()
                usersMain = parser.parse(users, recursive=True)
                usersFilter = [
                    "bio",
                    "tagline",
                    "cover_deviation",
                    "last_status",
                    "cover_photo",
                    "stats",
                    "user",
                ]
                embedVar = discord.Embed()
                try:
                    if "cover_deviation" in usersMain:
                        for keys, value in usersMain.items():
                            if keys not in usersFilter:
                                embedVar.add_field(
                                    name=keys, value=f"[{value}]", inline=True
                                )
                        for k, v in usersMain["stats"].items():
                            embedVar.add_field(name=k, value=f"[{v}]", inline=True)
                        embedVar.title = usersMain["user"]["username"]
                        embedVar.description = (
                            f"{usersMain['tagline']}\n\n{usersMain['bio']}"
                        )
                        embedVar.set_thumbnail(url=usersMain["user"]["usericon"])
                        embedVar.set_image(
                            url=usersMain["cover_deviation"]["cover_deviation"][
                                "content"
                            ]["src"]
                        )
                        await ctx.respond(embed=embedVar)
                    else:
                        for keys1, value1 in usersMain.items():
                            if keys1 not in usersFilter:
                                embedVar.add_field(
                                    name=keys1, value=f"[{value1}]", inline=True
                                )
                        for k1, v1 in usersMain["stats"].items():
                            embedVar.add_field(name=k1, value=f"[{v1}]", inline=True)
                        embedVar.title = usersMain["user"]["username"]
                        embedVar.description = (
                            f"{usersMain['tagline']}\n\n{usersMain['bio']}"
                        )
                        embedVar.set_thumbnail(url=usersMain["user"]["usericon"])
                        await ctx.respond(embed=embedVar)
                except Exception:
                    embedError = discord.Embed(
                        color=discord.Color.from_rgb(255, 214, 214)
                    )
                    embedError.description = "The query failed. Please try again"
                    embedError.add_field(
                        name="Error", value=usersMain["error"], inline=True
                    )
                    embedError.add_field(
                        name="Error Description",
                        value=usersMain["error_description"],
                        inline=True,
                    )
                    embedError.add_field(
                        name="Status", value=usersMain["status"], inline=True
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(DeviantArtV1(bot))
