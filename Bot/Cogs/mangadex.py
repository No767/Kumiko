import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from exceptions import NotFoundHTTPException

parser = simdjson.Parser()


class List(list):
    def __setitem__(self, id, data):
        super().__setitem__(id - 1, data)

    def __getitem__(self, id):
        return super().__getitem__(id - 1)


class MangaDexV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    md = SlashCommandGroup("mangadex", "Commmands for the MangaDex service")
    mdScanlation = md.create_subgroup(
        "scanlation", "Commands for the scanlation section"
    )

    @md.command(name="search")
    async def manga(self, ctx, *, manga: Option(str, "Name of Manga")):
        """Searches for up to 5 manga on MangaDex"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "title": manga,
                "publicationDemographic[]": "none",
                "contentRating[]": "safe",
                "order[title]": "asc",
                "limit": 5,
            }
            async with session.get(
                f"https://api.mangadex.org/manga/", params=params
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                embedVar = discord.Embed()
                mangaFilter = [
                    "tags",
                    "title",
                    "altTitles",
                    "description",
                    "links",
                    "background",
                ]
                try:
                    try:
                        if len(dataMain["data"]) == 0:
                            raise ValueError
                        else:
                            for dictItem in dataMain["data"]:
                                mangaID = dictItem["id"]
                                mangaTitle = [
                                    val6
                                    for _, val6 in dictItem["attributes"][
                                        "title"
                                    ].items()
                                ]
                                mainDesc = [
                                    val7
                                    for _, val7 in dictItem["attributes"][
                                        "description"
                                    ].items()
                                ]
                                for k, v in dictItem["attributes"].items():
                                    if k not in mangaFilter:
                                        embedVar.add_field(
                                            name=k, value=f"[{v}]", inline=True
                                        )
                                for item in dictItem["attributes"]["tags"]:
                                    embedVar.add_field(
                                        name="Tags",
                                        value=f'[{item["attributes"]["name"]["en"]}]',
                                        inline=True,
                                    )
                                for item1, res in dictItem["attributes"][
                                    "links"
                                ].items():
                                    embedVar.add_field(
                                        name=item1, value=f"[{res}]", inline=True
                                    )
                                for titles in dictItem["attributes"]["altTitles"]:
                                    for keys, values in titles.items():
                                        embedVar.add_field(
                                            name=keys, value=f"[{values}]", inline=True
                                        )
                                for item in dictItem["relationships"]:
                                    if item["type"] not in [
                                        "manga",
                                        "author",
                                        "artist",
                                    ]:
                                        coverArtID = item["id"]
                                        async with session.get(
                                            f"https://api.mangadex.org/cover/{coverArtID}"
                                        ) as rp:
                                            cover_art_data = await rp.json(
                                                loads=orjson.loads
                                            )
                                            cover_art = cover_art_data["data"][
                                                "attributes"
                                            ]["fileName"]
                                            embedVar.set_image(
                                                url=f"https://uploads.mangadex.org/covers/{mangaID}/{cover_art}"
                                            )
                                embedVar.title = (
                                    str(mangaTitle)
                                    .replace("'", "")
                                    .replace("[", "")
                                    .replace("]", "")
                                )
                                embedVar.description = (
                                    str(mainDesc)
                                    .replace("'", "")
                                    .replace("[", "")
                                    .replace("]", "")
                                )
                                await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedErrorAlt2 = discord.Embed()
                        embedErrorAlt2.description = "Sorry, but the manga you searched for does not exist or is invalid. Please try again."
                        await ctx.respond(embed=embedErrorAlt2)
                except Exception as e:
                    embedErrorAlt = discord.Embed()
                    embedErrorAlt.description = (
                        "Sorry, but there was an error. Please try again."
                    )
                    embedErrorAlt.add_field(name="Reason", value=e, inline=True)
                    embedErrorAlt.add_field(
                        name="HTTP Response Code", value=r.status, inline=True
                    )
                    await ctx.respond(embed=embedErrorAlt)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @md.command(name="random")
    async def manga_random(self, ctx):
        """Returns an random manga from MangaDex"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.mangadex.org/manga/random") as r:
                data2 = await r.content.read()
                dataMain2 = parser.parse(data2, recursive=True)
                mangaFilter2 = [
                    "tags",
                    "title",
                    "altTitles",
                    "description",
                    "links",
                    "background",
                ]
                tagFilter = ["id", "type", "relationships"]
                embedVar = discord.Embed()
                try:
                    try:
                        if r.status == 500:
                            embedErrorMain = discord.Embed()
                            embedErrorMain.description = "It seems like there is no manga to select from... Don't worry about it, just try again"
                            embedErrorMain.add_field(
                                name="HTTP Response Code", value=r.status, inline=True
                            )
                            await ctx.respond(embed=embedErrorMain)
                        elif len(dataMain2["data"]) == 0:
                            raise ValueError
                        else:
                            mangaTitle2 = [
                                val8
                                for _, val8 in dataMain2["data"]["attributes"][
                                    "title"
                                ].items()
                            ]
                            mainDesc2 = [
                                val9
                                for _, val9 in dataMain2["data"]["attributes"][
                                    "description"
                                ].items()
                            ]
                            for titles in dataMain2["data"]["attributes"]["altTitles"]:
                                allAltTitles = [value for _, value in titles.items()]
                            for k, v in dataMain2["data"]["attributes"].items():
                                if k not in mangaFilter2:
                                    embedVar.add_field(name=k, value=v, inline=True)
                            for keys, value in dataMain2["data"]["attributes"][
                                "links"
                            ].items():
                                embedVar.add_field(name=keys, value=value, inline=True)
                            for tagItem in dataMain2["data"]["attributes"]["tags"]:
                                mainTags = [
                                    v["name"]["en"]
                                    for k, v in tagItem.items()
                                    if k not in tagFilter
                                ]
                            for item in dataMain2["data"]["relationships"]:
                                mangaID2 = dataMain2["data"]["id"]
                                if item["type"] not in ["manga", "author", "artist"]:
                                    coverArtID2 = item["id"]
                                    async with session.get(
                                        f"https://api.mangadex.org/cover/{coverArtID2}"
                                    ) as rp:
                                        cover_art_data2 = await rp.json(
                                            loads=orjson.loads
                                        )
                                        cover_art2 = cover_art_data2["data"][
                                            "attributes"
                                        ]["fileName"]
                                        embedVar.set_image(
                                            url=f"https://uploads.mangadex.org/covers/{mangaID2}/{cover_art2}"
                                        )
                            embedVar.title = (
                                str(mangaTitle2)
                                .replace("'", "")
                                .replace("[", "")
                                .replace("]", "")
                            )
                            embedVar.description = (
                                str(mainDesc2)
                                .replace("'", "")
                                .replace("[", "")
                                .replace("]", "")
                            )
                            embedVar.add_field(
                                name="Alt Titles",
                                value=str(allAltTitles).replace("'", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Tags",
                                value=str(mainTags).replace("'", ""),
                                inline=True,
                            )
                            await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedValErrorMain = discord.Embed()
                        embedValErrorMain.description = "It seems like there wasn't any manga found. Please try again"
                        await ctx.respond(embed=embedValErrorMain)
                except Exception as e:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = "There was an error. Please try again."
                    embedErrorMain.add_field(name="Error", value=e, inline=True)
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mdScanlation.command(name="search")
    async def scanlation_search(
        self, ctx, *, name: Option(str, "The name of the scanlation group")
    ):
        """Returns up to 5 scanlation groups via the name given"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "limit": 5,
                "name": name,
                "order[name]": "asc",
                "order[relevance]": "desc",
            }
            async with session.get(
                "https://api.mangadex.org/group", params=params
            ) as totally_another_response:
                md_data2 = await totally_another_response.content.read()
                mdDataMain = parser.parse(md_data2, recursive=True)
                embed2 = discord.Embed()
                mdFilter = ["altNames", "description", "name"]
                try:
                    if len(mdDataMain["data"]) == 0:
                        embed1 = discord.Embed()
                        embed1.description = (
                            "Sorry, but no results were found... Please try again."
                        )
                        embed1.add_field(
                            name="Total", value=mdDataMain["total"], inline=True
                        )
                        embed1.add_field(
                            name="HTTP Status",
                            value=totally_another_response.status,
                            inline=True,
                        )
                        await ctx.respond(embed=embed1)

                    else:
                        for dictItem in mdDataMain["data"]:
                            embed2.title = dictItem["attributes"]["name"]
                            embed2.description = dictItem["attributes"]["description"]
                            for k, v in dictItem["attributes"].items():
                                if k not in mdFilter:
                                    embed2.add_field(name=k, value=v, inline=True)
                            await ctx.respond(embed=embed2)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mdScanlation.command(name="id")
    async def scanlation_id(
        self, ctx, *, scanlation_id: Option(str, "The ID of the scanlation group")
    ):
        """Returns the scanlation group with the ID given"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.mangadex.org/group/{scanlation_id}"
            ) as another_response:
                payload = await another_response.content.read()
                payloadMain = parser.parse(payload, recursive=True)
                print(payloadMain)
                try:
                    try:
                        if payloadMain["result"] == "error":
                            embed3 = discord.Embed()
                            embed3.description = (
                                "Sorry, but no results were found... Please try again."
                            )
                            await ctx.respond(embed=embed3)
                        elif len(payloadMain["data"]) == 0:
                            raise ValueError
                        else:
                            embed4 = discord.Embed()
                            mdFilter2 = ["altNames", "description", "name"]
                            embed4.title = payloadMain["data"]["attributes"]["name"]
                            embed4.description = payloadMain["data"]["attributes"][
                                "description"
                            ]
                            for k, v in payloadMain["data"]["attributes"].items():
                                if k not in mdFilter2:
                                    embed4.add_field(name=k, value=v, inline=True)
                            await ctx.respond(embed=embed4)
                    except ValueError:
                        embedValError = discord.Embed()
                        embedValError.description = (
                            "Hm, it seems like there are no results... Please try again"
                        )
                        await ctx.respond(embed=embedValError)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @md.command(name="user")
    async def user(self, ctx, *, user_id: Option(str, "The ID of the user")):
        """Searches up users on mangadex via id"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.mangadex.org/user/{user_id}") as rep:
                payload = await rep.content.read()
                payloadMain2 = orjson.loads(payload)
                try:
                    try:
                        if payloadMain2["result"] == "error":
                            embedError = discord.Embed()
                            embedError.description = (
                                "Sorry, but no results were found... Please try again."
                            )
                            await ctx.respond(embed=embedError)
                        elif len(payloadMain2["data"]) == 0:
                            raise ValueError
                        else:
                            embed = discord.Embed()
                            mainFilter = ["attributes", "relationships"]
                            embed.title = payloadMain2["data"]["attributes"]["username"]
                            for payloadKeys, payloadValues in payloadMain2[
                                "data"
                            ].items():
                                if payloadKeys not in mainFilter:
                                    embed.add_field(
                                        name=payloadKeys,
                                        value=payloadValues,
                                        inline=True,
                                    )
                            for k, v in payloadMain2["data"]["attributes"].items():
                                if k not in "username":
                                    embed.add_field(name=k, value=v, inline=True)
                            await ctx.respond(embed=embed)
                    except ValueError:
                        embedValError = discord.Embed()
                        embedValError.description = (
                            "Hm, it seems like there are no results... Please try again"
                        )
                        await ctx.respond(embed=embedValError)

                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @md.command(name="author")
    async def author(self, ctx, *, author_name: Option(str, "The name of the author")):
        """Returns up to 5 authors and their info"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"limit": 5, "name": author_name, "order[name]": "asc"}
            async with session.get(
                "https://api.mangadex.org/author", params=params
            ) as author_response:
                author_payload = await author_response.content.read()
                authorPayloadMain = parser.parse(author_payload, recursive=True)
                embedVar = discord.Embed()
                try:
                    try:
                        if len(authorPayloadMain["data"]) == 0:
                            raise ValueError
                        else:
                            authorFilter = ["imageUrl", "name", "biography"]
                            mainFilterV3 = ["attributes", "relationships", "type"]
                            for authorDictItem in authorPayloadMain["data"]:
                                embedVar.title = authorDictItem["attributes"]["name"]
                                embedVar.description = authorDictItem["attributes"][
                                    "biography"
                                ]
                                for keys, value in authorDictItem.items():
                                    if keys not in mainFilterV3:
                                        embedVar.add_field(
                                            name=keys, value=value, inline=True
                                        )
                                        embedVar.remove_field(17)
                                for k, v in authorDictItem["attributes"].items():
                                    if k not in authorFilter:
                                        embedVar.add_field(name=k, value=v, inline=True)
                                        embedVar.remove_field(17)

                                await ctx.respond(embed=embedVar)
                    except ValueError:
                        embedValError = discord.Embed()
                        embedValError.description = (
                            "Hm, it seems like there are no results... Please try again"
                        )
                        await ctx.respond(embed=embedValError)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        "The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @md.command(name="read")
    async def manga_read(
        self,
        ctx,
        *,
        manga_id: Option(str, "The Manga's ID"),
        chapter_number: Option(int, "The chapter number of the manga"),
    ):
        """Reads a chapter out of the manga provided on MangaDex"""
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                params = {
                    "contentRating[]": "safe",
                    "includeFutureUpdates": 1,
                    "order[createdAt]": "asc",
                    "order[updatedAt]": "asc",
                    "order[publishAt]": "asc",
                    "order[readableAt]": "asc",
                    "order[volume]": "asc",
                    "order[chapter]": "asc",
                }
                async with session.get(
                    f"https://api.mangadex.org/manga/{manga_id}/feed", params=params
                ) as r:
                    data = await r.content.read()
                    dataMain = parser.parse(data, recursive=True)
                    if "error" in dataMain["result"]:
                        raise NotFoundHTTPException
                    else:
                        chapterIndexID = List(dataMain["data"])[chapter_number]["id"]
                        chapterTitle = List(dataMain["data"])[chapter_number][
                            "attributes"
                        ]["title"]
                        chapterPos = List(dataMain["data"])[chapter_number][
                            "attributes"
                        ]["chapter"]
                        async with aiohttp.ClientSession(
                            json_serialize=orjson.dumps
                        ) as session:
                            async with session.get(
                                f"https://api.mangadex.org/at-home/server/{chapterIndexID}"
                            ) as r:
                                data2 = await r.content.read()
                                dataMain2 = parser.parse(data2, recursive=True)
                                if "error" in dataMain2["result"]:
                                    raise NotFoundHTTPException
                                else:
                                    chapter_hash = dataMain2["chapter"]["hash"]
                                    paginator = pages.Paginator(
                                        pages=[
                                            discord.Embed()
                                            .set_footer(
                                                text=f"{chapterTitle} - Chapter {chapterPos}"
                                            )
                                            .set_image(
                                                url=f"https://uploads.mangadex.org/data/{chapter_hash}/{item}"
                                            )
                                            for item in dataMain2["chapter"]["data"]
                                        ],
                                        loop_pages=True,
                                    )
                                    await paginator.respond(
                                        ctx.interaction, ephemeral=False
                                    )
        except NotFoundHTTPException:
            embedError = discord.Embed()
            embedError.description = "It seems like the manga's id is invalid or cannot be found. Please try again"
            await ctx.respond(embed=embedError)


def setup(bot):
    bot.add_cog(MangaDexV1(bot))
