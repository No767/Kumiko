import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from rin_exceptions import ItemNotFound, NoItemsError

jsonParser = simdjson.Parser()


class ModrinthV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    modrinth = SlashCommandGroup("modrinth", "Commands for Modrinth")
    mod = modrinth.create_subgroup("mod", "Commands for mods")
    modVersions = modrinth.create_subgroup("versions", "Commands for mod versions")
    modrinthUser = modrinth.create_subgroup("user", "Commands for users")

    @modrinth.command(name="search")
    async def modrinthSearch(
        self,
        ctx,
        *,
        mod: Option(str, "The name of the mod"),
        modloader: Option(
            str, "Forge or Fabric", choices=["Forge", "Fabric"], default="Forge"
        ),
    ):
        """Searches for up to 25 mods on Modrinth"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "query": mod,
                "index": "relevance",
                "limit": 25,
                "facets": f'[["categories:{str(modloader).lower()}"]]',
            }
            async with session.get(
                "https://api.modrinth.com/v2/search", params=params
            ) as r:
                data = await r.content.read()
                dataMain = jsonParser.parse(data, recursive=True)
                try:
                    if len(dataMain["hits"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=mainItem["title"],
                                    description=mainItem["description"],
                                )
                                .add_field(
                                    name="Author", value=mainItem["author"], inline=True
                                )
                                .add_field(
                                    name="Categories",
                                    value=mainItem["categories"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Versions",
                                    value=mainItem["versions"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Latest Version",
                                    value=mainItem["latest_version"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Date Created",
                                    value=parser.isoparse(
                                        mainItem["date_created"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Updated",
                                    value=parser.isoparse(
                                        mainItem["date_modified"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Downloads",
                                    value=mainItem["downloads"],
                                    inline=True,
                                )
                                .add_field(
                                    name="License",
                                    value=mainItem["license"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Mod URL",
                                    value=f"https://modrinth.com/mod/{mainItem['slug']}",
                                    inline=True,
                                )
                                .set_thumbnail(url=mainItem["icon_url"])
                                for mainItem in dataMain["hits"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = (
                        f"Sorry, but there are no mods named {mod}. Please try again"
                    )
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mod.command(name="list")
    async def modrinthProject(
        self,
        ctx,
        *,
        name: Option(str, "The name of the mod"),
        modloader: Option(
            str, "Forge or Fabric", choices=["Forge", "Fabric"], default="Forge"
        ),
    ):
        """Gets info about the mod requested"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "query": name,
                "index": "relevance",
                "limit": 1,
                "facets": f'[["categories:{str(modloader).lower()}"]]',
            }
            async with session.get(
                "https://api.modrinth.com/v2/search", params=params
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = jsonParser.parse(data, recursive=True)
                    if len(dataMain["hits"]) == 0:
                        raise NoItemsError
                    else:
                        projectID = dataMain["hits"][0]["project_id"]
                        async with aiohttp.ClientSession(
                            json_serialize=orjson.dumps
                        ) as session:
                            async with session.get(
                                f"https://api.modrinth.com/v2/project/{projectID}"
                            ) as res:
                                try:
                                    modData = await res.content.read()
                                    modDataMain = jsonParser.parse(
                                        modData, recursive=True
                                    )
                                    modDataFilter = [
                                        "versions",
                                        "license",
                                        "icon_url",
                                        "body",
                                        "title",
                                        "description",
                                        "donation_urls",
                                        "gallery",
                                        "moderator_message",
                                        "body_url",
                                        "published",
                                        "updated",
                                        "status",
                                        "id",
                                        "slug",
                                        "project_type",
                                        "team",
                                        "approved",
                                    ]
                                    embedVar = discord.Embed()
                                    for keys, value in modDataMain.items():
                                        if keys not in modDataFilter:
                                            embedVar.add_field(
                                                name=keys, value=value, inline=True
                                            )
                                    for item in modDataMain["gallery"]:
                                        embedVar.set_image(url=item["url"])
                                    for k, v in modDataMain["license"].items():
                                        embedVar.add_field(
                                            name=f"License {k}", value=v, inline=True
                                        )
                                    embedVar.set_thumbnail(url=modDataMain["icon_url"])
                                    embedVar.title = modDataMain["title"]
                                    embedVar.description = f"{modDataMain['description']}\n\n{modDataMain['body']}"
                                    embedVar.add_field(
                                        name="Publish Time",
                                        value=parser.isoparse(
                                            modDataMain["published"]
                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Updated Time",
                                        value=parser.isoparse(
                                            modDataMain["updated"]
                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                        inline=True,
                                    )
                                    embedVar.add_field(
                                        name="Mod URL",
                                        value=f"https://modrinth.com/mod/{modDataMain['slug']}",
                                        inline=True,
                                    )
                                    await ctx.respond(embed=embedVar)
                                except ValueError:
                                    embedError = discord.Embed()
                                    embedError.description = "Sorry, but the mod requested does not exists or couldn't be found. Please try again..."
                                    await ctx.respond(embed=embedError)
                except NoItemsError:
                    await ctx.respond(
                        embed=discord.Embed(
                            description="Sorry, but the mod requested could not be found. Please try again"
                        )
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modVersions.command(name="all")
    async def modrinthProjectVersion(
        self,
        ctx,
        *,
        name: Option(str, "The name of the mod or project"),
        game_version: Option(str, "The version of Minecraft"),
        loaders: Option(
            str,
            "The types of modloaders to filter out - Forge or Fabric",
            choices=["Forge", "Fabric"],
            default="Forge",
        ),
    ):
        """Lists out all of the versions for a mod"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "query": name,
                "index": "relevance",
                "limit": 1,
                "facets": f'[["categories:{str(loaders).lower()}"]]',
            }
            async with session.get(
                "https://api.modrinth.com/v2/search", params=params
            ) as r:
                try:
                    data = await r.content.read()
                    dataMain = jsonParser.parse(data, recursive=True)
                    if len(dataMain["hits"]) == 0:
                        raise ItemNotFound
                    else:
                        modID = dataMain["hits"][0]["project_id"]
                        async with aiohttp.ClientSession(
                            json_serialize=orjson.dumps
                        ) as session:
                            params = {
                                "loaders": f"[{str(loaders).lower()}]",
                                "game_versions": f"[{game_version}]",
                            }
                            async with session.get(
                                f"https://api.modrinth.com/v2/project/{modID}/version",
                                params=params,
                            ) as res:
                                versionData = await res.content.read()
                                try:
                                    versionDataMain = jsonParser.parse(
                                        versionData, recursive=True
                                    )
                                    try:
                                        if len(versionDataMain) == 0:
                                            raise NoItemsError
                                        else:
                                            mainPages = pages.Paginator(
                                                pages=[
                                                    discord.Embed(
                                                        title=mainItem["name"],
                                                        description=mainItem[
                                                            "changelog"
                                                        ],
                                                    )
                                                    .add_field(
                                                        name="Version Number",
                                                        value=str(
                                                            mainItem["version_number"]
                                                        ).replace("'", ""),
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Date Published",
                                                        value=parser.isoparse(
                                                            mainItem["date_published"]
                                                        ).strftime("%Y-%m-%d %H:%M:%S"),
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Downloads",
                                                        value=mainItem["downloads"],
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Version Type",
                                                        value=mainItem["version_type"],
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Game Versions",
                                                        value=str(
                                                            mainItem["game_versions"]
                                                        ).replace("'", ""),
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Dependencies",
                                                        value=[
                                                            items["file_name"]
                                                            for items in mainItem[
                                                                "dependencies"
                                                            ]
                                                        ]
                                                        if len(mainItem["dependencies"])
                                                        > 0
                                                        else "None",
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Loaders",
                                                        value=str(
                                                            mainItem["loaders"]
                                                        ).replace("'", ""),
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Download URL",
                                                        value=str(
                                                            [
                                                                items["url"]
                                                                for items in mainItem[
                                                                    "files"
                                                                ]
                                                            ]
                                                        ).replace("'", ""),
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Download SHA1 Hash",
                                                        value=str(
                                                            [
                                                                items["hashes"]["sha1"]
                                                                for items in mainItem[
                                                                    "files"
                                                                ]
                                                            ]
                                                        ).replace("'", ""),
                                                        inline=True,
                                                    )
                                                    .add_field(
                                                        name="Download SHA512 Hash",
                                                        value=str(
                                                            [
                                                                items["hashes"][
                                                                    "sha512"
                                                                ]
                                                                for items in mainItem[
                                                                    "files"
                                                                ]
                                                            ]
                                                        ).replace("'", ""),
                                                        inline=True,
                                                    )
                                                    for mainItem in versionDataMain
                                                ],
                                                loop_pages=True,
                                            )
                                            await mainPages.respond(
                                                ctx.interaction, ephemeral=False
                                            )

                                    except NoItemsError:
                                        embedErrorMain = discord.Embed()
                                        embedErrorMain.description = "Sorry, but it seems like there are no releases for the mod. Please try again"
                                        await ctx.respond(embed=embedErrorMain)
                                except ValueError:
                                    embedVarError = discord.Embed()
                                    embedVarError.description = "Sorry, but there was no such mod... Please try again..."
                                    await ctx.respond(embed=embedVarError)
                except ItemNotFound:
                    await ctx.respond(
                        embed=discord.Embed(
                            description="Sorry, but the mod requested could not be found. Please try again"
                        )
                    )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modrinthUser.command(name="search")
    async def modrinthUserMain(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """Returns info on the given user"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.modrinth.com/v2/user/{username}"
            ) as response:
                userData = await response.content.read()
                try:
                    userDataMain = jsonParser.parse(userData, recursive=True)
                    embedVar = discord.Embed()
                    userFilter = [
                        "bio",
                        "username",
                        "avatar_url",
                        "id",
                        "github_id",
                        "email",
                        "created",
                        "name",
                    ]
                    for userKeys, userValue in userDataMain.items():
                        if userKeys not in userFilter:
                            embedVar.add_field(
                                name=userKeys, value=userValue, inline=True
                            )
                    embedVar.title = userDataMain["username"]
                    embedVar.description = userDataMain["bio"]
                    embedVar.add_field(
                        name="created",
                        value=parser.isoparse(userDataMain["created"]).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        inline=True,
                    )
                    embedVar.set_thumbnail(url=userDataMain["avatar_url"])
                    await ctx.respond(embed=embedVar)
                except ValueError:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = "Sorry, but the user you were looking for doesn't exist. Please try again..."
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modrinthUser.command(name="projects")
    async def modrinthUserProjects(
        self, ctx, *, username: Option(str, "The username of the user")
    ):
        """Returns info on the given user's projects"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.modrinth.com/v2/user/{username}"
            ) as response:
                try:
                    userData = await response.content.read()
                    userDataMain = jsonParser.parse(userData, recursive=True)
                    userDataID = userDataMain["id"]
                    async with aiohttp.ClientSession(
                        json_serialize=orjson.dumps
                    ) as session:
                        async with session.get(
                            f"https://api.modrinth.com/v2/user/{userDataID}/projects"
                        ) as r:
                            data = await r.content.read()
                            dataMain6 = jsonParser.parse(data, recursive=True)
                            try:
                                if len(dataMain6) == 0:
                                    raise NoItemsError
                                else:
                                    mainPages = pages.Paginator(
                                        pages=[
                                            discord.Embed(
                                                title=mainItem["title"],
                                                description=mainItem["description"],
                                            )
                                            .add_field(
                                                name="Published Time",
                                                value=parser.isoparse(
                                                    mainItem["published"]
                                                ).strftime("%Y-%m-%d %H:%M:%S"),
                                                inline=True,
                                            )
                                            .add_field(
                                                name="Last Updated",
                                                value=parser.isoparse(
                                                    mainItem["updated"]
                                                ).strftime("%Y-%m-%d %H:%M:%S"),
                                                inline=True,
                                            )
                                            .add_field(
                                                name="License",
                                                value=mainItem["license"]["name"],
                                                inline=True,
                                            )
                                            .add_field(
                                                name="Downloads",
                                                value=mainItem["downloads"],
                                                inline=True,
                                            )
                                            .add_field(
                                                name="Categories",
                                                value=mainItem["categories"],
                                                inline=True,
                                            )
                                            .add_field(
                                                name="Mod URL",
                                                value=f"https://modrinth.com/mod/{mainItem['slug']}",
                                                inline=True,
                                            )
                                            .set_thumbnail(url=mainItem["icon_url"])
                                            for mainItem in dataMain6
                                        ],
                                        loop_pages=True,
                                    )
                                    await mainPages.respond(
                                        ctx.interaction, ephemeral=False
                                    )
                            except NoItemsError:
                                embedErrorMain = discord.Embed()
                                embedErrorMain.description = "Sorry, but apparently the user has no projects. Please try again..."
                                await ctx.respond(embed=embedErrorMain)
                except ValueError:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = "Sorry, but the user you were looking for doesn't exist. Please try again..."
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(ModrinthV1(bot))
