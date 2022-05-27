import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from exceptions import NoItemsError

parser = simdjson.Parser()


class ModrinthV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    modrinth = SlashCommandGroup("modrinth", "Commands for Modrinth")
    mod = modrinth.create_subgroup("mod", "Commands for mods")
    modVersions = modrinth.create_subgroup("versions", "Commands for mod versions")
    modrinthUser = modrinth.create_subgroup("user", "Commands for users")
    modrinthTeam = modrinth.create_subgroup("team", "Commands for teams")

    @modrinth.command(name="search")
    async def modrinthSearch(
        self,
        ctx,
        *,
        mod: Option(str, "The name of the mod"),
        modloader: Option(str, "Forge or Fabric"),
    ):
        """Searches for up to 5 mods on Modrinth"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "query": mod,
                "index": "relevance",
                "limit": 5,
                "facets": f'[["categories:{modloader}"]]',
            }
            async with session.get(
                "https://api.modrinth.com/v2/search", params=params
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data)
                modFilter = ["title", "gallery", "icon_url", "description"]
                embedVar = discord.Embed()
                try:
                    if len(dataMain["hits"]) == 0:
                        raise ValueError
                    for dictItem in dataMain["hits"]:
                        for k, v in dictItem.items():
                            if k not in modFilter:
                                embedVar.add_field(name=k, value=v, inline=True)
                                embedVar.remove_field(-13)
                        embedVar.title = dictItem["title"]
                        embedVar.description = dictItem["description"]
                        embedVar.set_thumbnail(url=dictItem["icon_url"])
                        await ctx.respond(embed=embedVar)
                except ValueError:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = (
                        f"Sorry, but there are no mods named {mod}. Please try again"
                    )
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mod.command(name="list")
    async def modrinthProject(
        self, ctx, *, mod_slug: Option(str, "The ID or slug of the project")
    ):
        """Gets info about the mod requested"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.modrinth.com/v2/project/{mod_slug}"
            ) as res:
                try:
                    modData = await res.content.read()
                    modDataMain = parser.parse(modData, recursive=True)
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
                    ]
                    embedVar = discord.Embed()
                    for keys, value in modDataMain.items():
                        if keys not in modDataFilter:
                            embedVar.add_field(name=keys, value=value, inline=True)
                    for item in modDataMain["gallery"]:
                        embedVar.set_image(url=item["url"])
                    for k, v in modDataMain["license"].items():
                        embedVar.add_field(name=f"License {k}", value=v, inline=True)
                    embedVar.set_thumbnail(url=modDataMain["icon_url"])
                    embedVar.title = modDataMain["title"]
                    embedVar.description = (
                        f"{modDataMain['description']}\n\n{modDataMain['body']}"
                    )
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sorry, but the query could not be made. Please try again..."
                    )
                    embedError.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modVersions.command(name="all")
    async def modrinthProjectVersion(
        self,
        ctx,
        *,
        mod_name: Option(str, "The name of the mod or project"),
        loaders: Option(
            str,
            "The types of modloaders to filter out - Forge or Fabric",
            required=False,
            choices=["Forge", "Fabric"],
        ),
        game_version: Option(str, "The version of Minecraft", required=False),
    ):
        """Lists out all of the versions for a mod (may cause spam)"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "loaders": f"[{str(loaders).lower()}]",
                "game_versions": f"[{game_version}]",
            }
            async with session.get(
                f"https://api.modrinth.com/v2/project/{mod_name}/version", params=params
            ) as res:
                versionData = await res.content.read()
                try:
                    versionDataMain = parser.parse(versionData, recursive=True)
                    versionFilter = [
                        "changelog",
                        "name",
                        "dependencies",
                        "files",
                        "id",
                        "project_id",
                        "author_id",
                    ]
                    embedVar = discord.Embed()
                    try:
                        if len(versionDataMain) == 0:
                            raise NoItemsError
                        else:
                            for dictVersions in versionDataMain:
                                for keys, value in dictVersions.items():
                                    if keys not in versionFilter:
                                        embedVar.add_field(
                                            name=keys, value=value, inline=True
                                        )
                                        embedVar.remove_field(-14)
                                for fileItems in dictVersions["files"]:
                                    for k, v in fileItems.items():
                                        if k not in "hashes":
                                            embedVar.add_field(
                                                name=k, value=v, inline=True
                                            )
                                            embedVar.remove_field(-14)
                                    for hashKey, hashValue in fileItems[
                                        "hashes"
                                    ].items():
                                        embedVar.add_field(
                                            name=hashKey, value=hashValue, inline=True
                                        )
                                        embedVar.remove_field(-14)
                                embedVar.title = dictVersions["name"]
                                embedVar.description = dictVersions["changelog"]
                                await ctx.respond(embed=embedVar)
                    except NoItemsError:
                        embedErrorMain = discord.Embed()
                        embedErrorMain.description = "Sorry, but it seems like there are no releases for the mod. Please try again"
                        await ctx.respond(embed=embedErrorMain)
                except Exception as e:
                    embedVarError = discord.Embed()
                    embedVarError.description = (
                        "Sorry, but the query could not be made. Please try again..."
                    )
                    embedVarError.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVarError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modVersions.command(name="id")
    async def modrinthModVersion(
        self, ctx, *, mod_version_id: Option(str, "The ID of the mod version")
    ):
        """Returns info on the given mod version ID"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.modrinth.com/v2/version/{mod_version_id}"
            ) as r:
                data = await r.content.read()
                versionFilter = ["changelog", "name", "dependencies", "files"]
                embedVar = discord.Embed()
                try:
                    dataMain3 = parser.parse(data, recursive=True)
                    for keys, value in dataMain3.items():
                        if keys not in versionFilter:
                            embedVar.add_field(name=keys, value=value, inline=True)
                    for fileItems in dataMain3["files"]:
                        for k, v in fileItems.items():
                            if k not in "hashes":
                                embedVar.add_field(name=k, value=v, inline=True)
                        for hashKey, hashValue in fileItems["hashes"].items():
                            embedVar.add_field(
                                name=hashKey, value=hashValue, inline=True
                            )
                    embedVar.title = dataMain3["name"]
                    embedVar.description = dataMain3["changelog"]
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar.description = (
                        "Sorry, but the query could not be made. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modrinthUser.command(name="search")
    async def modrinthUserMain(
        self, ctx, *, username: Option(str, "The username or ID of the user")
    ):
        """Returns info on the given user"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.modrinth.com/v2/user/{username}"
            ) as response:
                userData = await response.content.read()
                try:
                    userDataMain = parser.parse(userData, recursive=True)
                    embedVar = discord.Embed()
                    userFilter = ["bio", "username", "avatar_url"]
                    for userKeys, userValue in userDataMain.items():
                        if userKeys not in userFilter:
                            embedVar.add_field(
                                name=userKeys, value=userValue, inline=True
                            )
                    embedVar.title = userDataMain["username"]
                    embedVar.description = userDataMain["bio"]
                    embedVar.set_thumbnail(url=userDataMain["avatar_url"])
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = (
                        "Sorry, but the query could not be made. Please try again..."
                    )
                    embedErrorMain.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modrinthUser.command(name="projects")
    async def modrinthUserProjects(
        self, ctx, *, username: Option(str, "The username or ID of the user")
    ):
        """Returns info on the given user's projects"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.modrinth.com/v2/user/{username}/projects"
            ) as r:
                data = await r.content.read()

                userProjectsFilter = [
                    "body",
                    "license",
                    "title",
                    "description",
                    "icon_url",
                    "versions",
                    "donation_urls",
                    "gallery",
                ]
                embedVar = discord.Embed()
                try:
                    dataMain6 = parser.parse(data, recursive=True)
                    try:
                        if len(dataMain6) == 0:
                            raise ValueError
                        else:
                            for dictProjects in dataMain6:
                                for keys, value in dictProjects.items():
                                    if keys not in userProjectsFilter:
                                        embedVar.add_field(
                                            name=keys, value=value, inline=True
                                        )
                                for licenseItem, licenseRes in dictProjects[
                                    "license"
                                ].items():
                                    embedVar.add_field(
                                        name=f"License {licenseItem}",
                                        value=licenseRes,
                                        inline=True,
                                    )
                                embedVar.title = dictProjects["title"]
                                embedVar.description = dictProjects["description"]
                                embedVar.set_thumbnail(url=dictProjects["icon_url"])
                                await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedErrorMain = discord.Embed()
                        embedErrorMain.description = "Sorry, but apparently the user has no projects. Please try again..."
                        await ctx.respond(embed=embedErrorMain)
                except Exception as e:
                    embedVar.description = (
                        "Sorry, but the query could not be made. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modrinthTeam.command(name="project")
    async def modrinthProjectTeamMembers(
        self, ctx, *, project: Option(str, "The slug or ID of the project")
    ):
        """Returns the team members of a project"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.modrinth.com/v2/project/{project}/members"
            ) as r:
                projectData = await r.content.read()
                projectDataMain = parser.parse(projectData, recursive=True)
                projectTeamFilter = ["bio", "avatar_url", "username"]
                embedVar = discord.Embed()
                try:
                    for dictTeam in projectDataMain:
                        for keys, value in dictTeam.items():
                            if keys not in "user":
                                embedVar.add_field(name=keys, value=value, inline=True)
                        for k, v in dictTeam["user"].items():
                            if k not in projectTeamFilter:
                                embedVar.add_field(name=k, value=v, inline=True)
                        embedVar.title = dictTeam["user"]["username"]
                        embedVar.description = dictTeam["user"]["bio"]
                        embedVar.set_thumbnail(url=dictTeam["user"]["avatar_url"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar.description = (
                        "Sorry, but the query could not be made. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @modrinthTeam.command(name="members")
    async def modrinthTeamMembers(
        self, ctx, *, team_id: Option(str, "The ID of the team")
    ):
        """Returns the members within the given team"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.modrinth.com/v2/team/{team_id}/members"
            ) as r:
                teamData = await r.content.read()
                teamDataMain = parser.parse(teamData, recursive=True)
                teamFilter = ["bio", "avatar_url", "username"]
                embedVar = discord.Embed()
                try:
                    for dictTeam2 in teamDataMain:
                        for keys, value in dictTeam2.items():
                            if keys not in "user":
                                embedVar.add_field(name=keys, value=value, inline=True)
                        for k, v in dictTeam2["user"].items():
                            if k not in teamFilter:
                                embedVar.add_field(name=k, value=v, inline=True)
                        embedVar.title = dictTeam2["user"]["username"]
                        embedVar.description = dictTeam2["user"]["bio"]
                        embedVar.set_thumbnail(url=dictTeam2["user"]["avatar_url"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar.description = (
                        "Sorry, but the query could not be made. Please try again..."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(ModrinthV1(bot))
