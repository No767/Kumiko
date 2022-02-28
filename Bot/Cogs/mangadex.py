import asyncio

import aiohttp
import discord
import orjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands


class MangaDexV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="mangadex-search",
        description="Searches for up to 5 manga on MangaDex",
        guild_ids=[866199405090308116],
    )
    async def manga(self, ctx, *, manga: Option(str, "Name of Manga")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            try:
                params = {
                    "title": manga,
                    "publicationDemographic[]": "none",
                    "contentRating[]": "safe",
                    "order[title]": "asc",
                    "limit": 5,
                }
                async with session.get(
                    "https://api.mangadex.org/manga/", params=params
                ) as r:
                    data = await r.json()
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
                        for dictItem in data["data"]:
                            mangaID = dictItem["id"]
                            mangaTitle = [
                                val6
                                for keys6, val6 in dictItem["attributes"][
                                    "title"
                                ].items()
                            ]
                            mainDesc = [
                                val7
                                for keys7, val7 in dictItem["attributes"][
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
                            for item1, res in dictItem["attributes"]["links"].items():
                                embedVar.add_field(
                                    name=item1, value=f"[{res}]", inline=True
                                )
                            for titles in dictItem["attributes"]["altTitles"]:
                                for keys, values in titles.items():
                                    embedVar.add_field(
                                        name=keys, value=f"[{values}]", inline=True
                                    )
                            for item in dictItem["relationships"]:
                                if item["type"] not in ["manga", "author", "artist"]:
                                    coverArtID = item["id"]
                                    async with session.get(
                                        f"https://api.mangadex.org/cover/{coverArtID}"
                                    ) as rp:
                                        cover_art_data = await rp.json()
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
                    except Exception as e:
                        embedErrorAlt = discord.Embed()
                        embedErrorAlt.description = (
                            "Sorry, but there was an error. Please try again."
                        )
                        embedErrorAlt.add_field(
                            name="Reason", value=e, inline=True)
                        embedErrorAlt.add_field(
                            name="HTTP Response Code", value=r.status, inline=True
                        )
                        await ctx.respond(embed=embedErrorAlt)

            except Exception as e:
                embedVar = discord.Embed()
                embedVar.description = (
                    "Sadly this command didn't work. Please try again"
                )
                embedVar.add_field(name="Reason", value=e, inline=True)
                await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="mangadex-random",
        description="Returns a random manga from MangaDex",
        guild_ids=[866199405090308116],
    )
    async def manga_random(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.mangadex.org/manga/random") as r:
                data = await r.json()
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
                    if r.status == 500:
                        embedErrorMain = discord.Embed()
                        embedErrorMain.description = "It seems like there is no manga to select from... Don't worry about it, just try again"
                        embedErrorMain.add_field(
                            name="HTTP Response Code", value=r.status, inline=True
                        )
                        await ctx.respond(embed=embedErrorMain)
                    else:
                        mangaTitle2 = [
                            val8
                            for keys8, val8 in data["data"]["attributes"][
                                "title"
                            ].items()
                        ]
                        mainDesc2 = [
                            val9
                            for keys9, val9 in data["data"]["attributes"][
                                "description"
                            ].items()
                        ]
                        for titles in data["data"]["attributes"]["altTitles"]:
                            allAltTitles = [value for keys,
                                            value in titles.items()]
                        for k, v in data["data"]["attributes"].items():
                            if k not in mangaFilter2:
                                embedVar.add_field(
                                    name=k, value=v, inline=True)
                        for keys, value in data["data"]["attributes"]["links"].items():
                            embedVar.add_field(
                                name=keys, value=value, inline=True)
                        for tagItem in data["data"]["attributes"]["tags"]:
                            mainTags = [
                                v["name"]["en"]
                                for k, v in tagItem.items()
                                if k not in tagFilter
                            ]
                        for item in data["data"]["relationships"]:
                            mangaID2 = data["data"]["id"]
                            if item["type"] not in ["manga", "author", "artist"]:
                                coverArtID2 = item["id"]
                                async with session.get(
                                    f"https://api.mangadex.org/cover/{coverArtID2}"
                                ) as rp:
                                    cover_art_data2 = await rp.json()
                                    cover_art2 = cover_art_data2["data"]["attributes"][
                                        "fileName"
                                    ]
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
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = (
                        "Sorry, but something went wrong... Please try again"
                    )
                    embedError.add_field(name="Reason", value=e, inline=True)
                    embedError.add_field(
                        name="HTTP Response Code", value=r.status, inline=True
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="mangadex-scanlation-search",
        description="Returns info about a scanlation group on MangaDex",
        guild_ids=[866199405090308116],
    )
    async def scanlation_search(
        self, ctx, *, name: Option(str, "The name of the scanlation group")
    ):
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
                md_data2 = await totally_another_response.json()
                embed2 = discord.Embed()
                mdFilter = ["altNames", "description", "name"]
                try:
                    if md_data2["data"] is None:
                        embed1 = discord.Embed()
                        embed1.description = (
                            "Sorry, but no results were found... Please try again."
                        )
                        embed1.add_field(
                            name="Total", value=md_data2["total"], inline=True
                        )
                        embed1.add_field(
                            name="HTTP Status",
                            value=totally_another_response.status,
                            inline=True,
                        )
                        await ctx.respond(embed=embed1)
                    else:
                        for dictItem in md_data2["data"]:
                            embed2.title = dictItem["attributes"]["name"]
                            embed2.description = dictItem["attributes"]["description"]
                            for k, v in dictItem["attributes"].items():
                                if k not in mdFilter:
                                    embed2.add_field(
                                        name=k, value=v, inline=True)
                            await ctx.respond(embed=embed2)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="mangadex-scanlation-id",
        description="Returns info about a scanlation group on MangaDex (Done via ID)",
        guild_ids=[866199405090308116],
    )
    async def scanlation_id(
        self, ctx, *, scanlation_id: Option(str, "The ID of the scanlation group")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.mangadex.org/group/{scanlation_id}"
            ) as another_response:
                payload = await another_response.json()
                try:
                    if payload["data"] is None:
                        embed3 = discord.Embed()
                        embed3.description = (
                            "Sorry, but no results were found... Please try again."
                        )
                        embed3.add_field(
                            name="Total", value=payload["total"], inline=True
                        )
                        embed3.add_field(
                            name="HTTP Status",
                            value=another_response.status,
                            inline=True,
                        )
                        await ctx.respond(embed=embed3)
                    else:
                        embed4 = discord.Embed()
                        mdFilter2 = ["altNames", "description", "name"]
                        embed4.title = payload["data"]["attributes"]["name"]
                        embed4.description = payload["data"]["attributes"][
                            "description"
                        ]
                        for k, v in payload["data"]["attributes"].items():
                            if k not in mdFilter2:
                                embed4.add_field(name=k, value=v, inline=True)
                        await ctx.respond(embed=embed4)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="mangadex-user",
        description="Returns info about a user on MangaDex",
        guild_ids=[866199405090308116],
    )
    async def user(self, ctx, *, user_id: Option(str, "The ID of the user")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.mangadex.org/user/{user_id}") as rep:
                payload = await rep.json()
                try:
                    embed = discord.Embed()
                    mainFilter = ["attributes", "relationships"]
                    embed.title = payload["data"]["attributes"]["username"]
                    for payloadKeys, payloadValues in payload["data"].items():
                        if payloadKeys not in mainFilter:
                            embed.add_field(
                                name=payloadKeys, value=payloadValues, inline=True
                            )
                    for k, v in payload["data"]["attributes"].items():
                        if k not in "username":
                            embed.add_field(name=k, value=v, inline=True)
                    await ctx.respond(embed=embed)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV6(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="mangadex-author",
        description="Returns info about an author on MangaDex",
        guild_ids=[866199405090308116],
    )
    async def author(self, ctx, *, author_name: Option(str, "The name of the author")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"limit": 5, "name": author_name, "order[name]": "asc"}
            async with session.get(
                "https://api.mangadex.org/author", params=params
            ) as author_response:
                author_payload = await author_response.json()
                embedVar = discord.Embed()
                try:
                    authorFilter = ["imageUrl", "name", "biography"]
                    mainFilterV3 = ["attributes", "relationships", "type"]
                    for authorDictItem in author_payload["data"]:
                        embedVar.title = authorDictItem["attributes"]["name"]
                        embedVar.description = authorDictItem["attributes"]["biography"]
                        for keys, value in authorDictItem.items():
                            if keys not in mainFilterV3:
                                embedVar.add_field(
                                    name=keys, value=value, inline=True)
                                embedVar.remove_field(17)
                        for k, v in authorDictItem["attributes"].items():
                            if k not in authorFilter:
                                embedVar.add_field(
                                    name=k, value=v, inline=True)
                                embedVar.remove_field(17)

                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexReaderV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Note that the MangaDex Reader has been saved for another release. v2.0.0 will not contain the mangadex reader
    # Later this should allow for the name to be inputted, but for now it purely relies on the chapter id
    @commands.command(name="mangadex-read", aliases=["md-read"])
    async def manga_read(self, ctx, *, id: str):
        try:
            async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
                async with session.get(f"https://api.mangadex.org/chapter/{id}") as r:
                    data = await r.json()
                    chapter_hash = data["data"]["attributes"]["hash"]
                    var = 0
                    var += 1
                    list_of_images = data["data"]["attributes"]["data"][var]
                    len(data["data"]["attributes"]["data"])
                    chapter_name = data["data"]["attributes"]["title"]
                    chapter_num = data["data"]["attributes"]["chapter"]
                    manga_id = data["data"]["relationships"][1]["id"]
                    async with session.get(
                        f"https://api.mangadex.org/manga/{manga_id}"
                    ) as resp:
                        data1 = await resp.json()
                        title = data1["data"]["attributes"]["title"]["en"]
                        embedVar = discord.Embed(
                            title=f"{title}",
                            color=discord.Color.from_rgb(231, 173, 255),
                        )
                        embedVar.description = f"{chapter_name} - Chapter {chapter_num}"
                        embedVar.set_image(
                            url=f"https://uploads.mangadex.org/data/{chapter_hash}/{list_of_images}"
                        )
                        await ctx.send(embed=embedVar)
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(MangaDexV1(bot))
    bot.add_cog(MangaDexV2(bot))
    bot.add_cog(MangaDexV3(bot))
    bot.add_cog(MangaDexV4(bot))
    bot.add_cog(MangaDexV5(bot))
    bot.add_cog(MangaDexV6(bot))
