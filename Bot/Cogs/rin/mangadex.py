import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from rin_exceptions import NoItemsError

jsonParser = simdjson.Parser()


class List(list):
    def __setitem__(self, id, data):
        super().__setitem__(id - 1, data)

    def __getitem__(self, id):
        return super().__getitem__(id - 1)


class MangaDex(commands.Cog):
    """Commands for getting data from MangaDex"""

    def __init__(self, bot):
        self.bot = bot

    md = SlashCommandGroup("mangadex", "Commmands for the MangaDex service")
    mdSearch = md.create_subgroup("search", "Search for stuff on MangaDex")
    mdScanlation = md.create_subgroup(
        "scanlation", "Commands for the scanlation section"
    )

    @mdSearch.command(name="manga")
    async def manga(self, ctx, *, manga: Option(str, "Name of Manga")):
        """Searches for up to 25 manga on MangaDex"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "title": manga,
                "publicationDemographic[]": "none",
                "contentRating[]": "safe",
                "order[title]": "asc",
                "limit": 25,
                "includes[]": "cover_art",
            }
            async with session.get(
                f"https://api.mangadex.org/manga/", params=params
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
                                    title=mainItem["attributes"]["title"]["en"]
                                    if "en" in mainItem["attributes"]["title"]
                                    else mainItem["attributes"]["title"],
                                    description=mainItem["attributes"]["description"][
                                        "en"
                                    ]
                                    if "en" in mainItem["attributes"]["description"]
                                    else mainItem["attributes"]["description"],
                                )
                                .add_field(
                                    name="Original Language",
                                    value=f'[{mainItem["attributes"]["originalLanguage"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Volume",
                                    value=f'[{mainItem["attributes"]["lastVolume"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Chapter",
                                    value=f'[{mainItem["attributes"]["lastChapter"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Status",
                                    value=f'[{mainItem["attributes"]["status"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Year",
                                    value=f'[{mainItem["attributes"]["year"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Content Rating",
                                    value=f'[{mainItem["attributes"]["contentRating"]}]',
                                    inline=True,
                                )
                                .add_field(
                                    name="Created At",
                                    value=parser.isoparse(
                                        mainItem["attributes"]["createdAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Updated At",
                                    value=parser.isoparse(
                                        mainItem["attributes"]["updatedAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Available Translated Language",
                                    value=f'{mainItem["attributes"]["availableTranslatedLanguages"]}'.replace(
                                        "'", ""
                                    ),
                                    inline=True,
                                )
                                .add_field(
                                    name="Tags",
                                    value=str(
                                        [
                                            str(
                                                [
                                                    val
                                                    for _, val in items["attributes"][
                                                        "name"
                                                    ].items()
                                                ]
                                            )
                                            .replace("[", "")
                                            .replace("]", "")
                                            .replace("'", "")
                                            for items in mainItem["attributes"]["tags"]
                                        ]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="MangaDex URL",
                                    value=f'https://mangadex.org/title/{mainItem["id"]}',
                                    inline=True,
                                )
                                .set_image(
                                    url=str(
                                        [
                                            f'https://uploads.mangadex.org/covers/{mainItem["id"]}/{items["attributes"]["fileName"]}'
                                            for items in mainItem["relationships"]
                                            if items["type"]
                                            not in ["manga", "author", "artist"]
                                        ]
                                    )
                                    .replace("'", "")
                                    .replace("[", "")
                                    .replace("]", "")
                                )
                                for mainItem in dataMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedErrorAlt2 = discord.Embed()
                    embedErrorAlt2.description = "Sorry, but the manga you searched for does not exist or is invalid. Please try again."
                    await ctx.respond(embed=embedErrorAlt2)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @md.command(name="random")
    async def manga_random(self, ctx):
        """Returns an random manga from MangaDex"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.mangadex.org/manga/random") as r:
                data2 = await r.content.read()
                dataMain2 = jsonParser.parse(data2, recursive=True)
                mangaFilter2 = [
                    "tags",
                    "title",
                    "altTitles",
                    "description",
                    "links",
                    "background",
                    "createdAt",
                    "updatedAt",
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
                            mangaTitle2 = (
                                dataMain2["data"]["attributes"]["title"]["en"]
                                if "en" in dataMain2["data"]["attributes"]["title"]
                                else dataMain2["data"]["attributes"]["title"]
                            )
                            mainDesc2 = (
                                dataMain2["data"]["attributes"]["description"]["en"]
                                if "en"
                                in dataMain2["data"]["attributes"]["description"]
                                else dataMain2["data"]["attributes"]["description"]
                            )
                            for k, v in dataMain2["data"]["attributes"].items():
                                if k not in mangaFilter2:
                                    embedVar.add_field(
                                        name=k, value=f"[{v}]", inline=True
                                    )
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
                                value=str(
                                    [
                                        v
                                        for items in dataMain2["data"]["attributes"][
                                            "altTitles"
                                        ]
                                        for k, v in items.items()
                                    ]
                                ).replace("'", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Tags",
                                value=str(mainTags).replace("'", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="MangaDex URL",
                                value=f'https://mangadex.org/title/{dataMain2["data"]["id"]}',
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

    @mdSearch.command(name="scanlation")
    async def scanlation_search(
        self, ctx, *, name: Option(str, "The name of the scanlation group")
    ):
        """Returns up to 25 scanlation groups via the name given"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "limit": 25,
                "name": name,
                "order[name]": "asc",
                "order[relevance]": "desc",
            }
            async with session.get(
                "https://api.mangadex.org/group", params=params
            ) as totally_another_response:
                md_data2 = await totally_another_response.content.read()
                mdDataMain = jsonParser.parse(md_data2, recursive=True)
                try:
                    if len(mdDataMain["data"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=mainItem["attributes"]["name"],
                                    description=mainItem["attributes"]["description"],
                                )
                                .add_field(
                                    name="Alt Names",
                                    value=mainItem["attributes"]["altNames"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Website",
                                    value=mainItem["attributes"]["website"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Discord",
                                    value=f'https://discord.gg/{mainItem["attributes"]["discord"]}'
                                    if mainItem["attributes"]["discord"] is not None
                                    else "None",
                                    inline=True,
                                )
                                .add_field(
                                    name="Twitter",
                                    value=f'https://twitter.com/{mainItem["attributes"]["twitter"]}'
                                    if mainItem["attributes"]["twitter"] is not None
                                    else "None",
                                    inline=True,
                                )
                                .add_field(
                                    name="Contact Email",
                                    value=mainItem["attributes"]["contactEmail"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Created At",
                                    value=parser.isoparse(
                                        mainItem["attributes"]["createdAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Updated At",
                                    value=parser.isoparse(
                                        mainItem["attributes"]["updatedAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                for mainItem in mdDataMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embed1 = discord.Embed()
                    embed1.description = (
                        "Sorry, but no results were found... Please try again."
                    )
                    await ctx.respond(embed=embed1)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mdSearch.command(name="author")
    async def author(self, ctx, *, author_name: Option(str, "The name of the author")):
        """Returns up to 25 authors and their info"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"limit": 25, "name": author_name, "order[name]": "asc"}
            async with session.get(
                "https://api.mangadex.org/author", params=params
            ) as author_response:
                author_payload = await author_response.content.read()
                authorPayloadMain = jsonParser.parse(author_payload, recursive=True)
                try:
                    if len(authorPayloadMain["data"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=mainItem["attributes"]["name"],
                                    description=mainItem["attributes"]["biography"],
                                )
                                .add_field(
                                    name="Created At",
                                    value=parser.isoparse(
                                        mainItem["attributes"]["createdAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Updated At",
                                    value=parser.isoparse(
                                        mainItem["attributes"]["updatedAt"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Twitter",
                                    value=mainItem["attributes"]["twitter"]
                                    if mainItem["attributes"]["twitter"] is not None
                                    else "None",
                                    inline=True,
                                )
                                .add_field(
                                    name="Pixiv",
                                    value=mainItem["attributes"]["pixiv"]
                                    if mainItem["attributes"]["pixiv"] is not None
                                    else "None",
                                    inline=True,
                                )
                                .add_field(
                                    name="YouTube",
                                    value=mainItem["attributes"]["youtube"]
                                    if mainItem["attributes"]["youtube"] is not None
                                    else "None",
                                    inline=True,
                                )
                                .add_field(
                                    name="Website",
                                    value=mainItem["attributes"]["website"],
                                    inline=True,
                                )
                                for mainItem in authorPayloadMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedValError = discord.Embed()
                    embedValError.description = (
                        "Hm, it seems like there are no results... Please try again"
                    )
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    # This will be disabled on production releases, since
    # this requires an ID input, and is not finished yet.
    # discord labs would definitely complain about this command...

    # @md.command(name="read")
    # async def manga_read(
    #     self,
    #     ctx,
    #     *,
    #     manga_id: Option(str, "The Manga's ID"),
    #     chapter_number: Option(int, "The chapter number of the manga"),
    # ):
    #     """Reads a chapter out of the manga provided on MangaDex"""
    #     try:
    #         async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
    #             params = {
    #                 "contentRating[]": "safe",
    #                 "includeFutureUpdates": 1,
    #                 "order[createdAt]": "asc",
    #                 "order[updatedAt]": "asc",
    #                 "order[publishAt]": "asc",
    #                 "order[readableAt]": "asc",
    #                 "order[volume]": "asc",
    #                 "order[chapter]": "asc",
    #             }
    #             async with session.get(
    #                 f"https://api.mangadex.org/manga/{manga_id}/feed", params=params
    #             ) as r:
    #                 data = await r.content.read()
    #                 dataMain = jsonParser.parse(data, recursive=True)
    #                 if "error" in dataMain["result"]:
    #                     raise NotFoundHTTPException
    #                 else:
    #                     chapterIndexID = List(dataMain["data"])[chapter_number]["id"]
    #                     chapterTitle = List(dataMain["data"])[chapter_number][
    #                         "attributes"
    #                     ]["title"]
    #                     chapterPos = List(dataMain["data"])[chapter_number][
    #                         "attributes"
    #                     ]["chapter"]
    #                     async with aiohttp.ClientSession(
    #                         json_serialize=orjson.dumps
    #                     ) as session:
    #                         async with session.get(
    #                             f"https://api.mangadex.org/at-home/server/{chapterIndexID}"
    #                         ) as r:
    #                             data2 = await r.content.read()
    #                             dataMain2 = jsonParser.parse(data2, recursive=True)
    #                             if "error" in dataMain2["result"]:
    #                                 raise NotFoundHTTPException
    #                             else:
    #                                 chapter_hash = dataMain2["chapter"]["hash"]
    #                                 paginator = pages.Paginator(
    #                                     pages=[
    #                                         discord.Embed()
    #                                         .set_footer(
    #                                             text=f"{chapterTitle} - Chapter {chapterPos}"
    #                                         )
    #                                         .set_image(
    #                                             url=f"https://uploads.mangadex.org/data/{chapter_hash}/{item}"
    #                                         )
    #                                         for item in dataMain2["chapter"]["data"]
    #                                     ],
    #                                     loop_pages=True,
    #                                 )
    #                                 await paginator.respond(
    #                                     ctx.interaction, ephemeral=False
    #                                 )
    #     except NotFoundHTTPException:
    #         embedError = discord.Embed()
    #         embedError.description = "It seems like the manga's id is invalid or cannot be found. Please try again"
    #         await ctx.respond(embed=embedError)


def setup(bot):
    bot.add_cog(MangaDex(bot))
