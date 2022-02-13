import asyncio
import os

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

MangaDex_API_Key = os.getenv("MangaDex_Access_Token")


class MangaDexV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-search", aliases=["md-search"])
    async def manga(self, ctx, *, manga: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            try:
                params = {
                    "title": manga,
                    "publicationDemographic[]": "none",
                    "contentRating[]": "safe",
                    "order[title]": "asc",
                }
                async with session.get(
                    f"https://api.mangadex.org/manga/", params=params
                ) as r:
                    data = await r.json()
                    id = data["data"][0]["id"]
                    async with session.get(
                        f'https://api.mangadex.org/manga/{id}?includes["cover_art"]&contentRating["safe"]&order[title]=asc'
                    ) as resp:
                        md_data = await resp.json()
                        cover_art_id = md_data["data"]["relationships"][2]["id"]
                        async with session.get(
                            f"https://api.mangadex.org/cover/{cover_art_id}"
                        ) as rp:
                            cover_art_data = await rp.json()
                            cover_art = cover_art_data["data"]["attributes"]["fileName"]
                            if "en" in data["data"][0]["attributes"]["title"]:
                                embedVar = discord.Embed()
                                embedVar.title = md_data["data"]["attributes"]["title"][
                                    "en"
                                ]
                                embedVar.description = (
                                    str(
                                        md_data["data"]["attributes"]["description"][
                                            "en"
                                        ]
                                    )
                                    .replace("\n", "")
                                    .replace("\r", "")
                                    .replace("'", "")
                                )
                                embedVar.add_field(
                                    name="Alt Titles",
                                    value=str(
                                        [
                                            title["en"]
                                            for title in md_data["data"]["attributes"][
                                                "altTitles"
                                            ]
                                        ]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                embedVar.add_field(
                                    name="Publication Demographics",
                                    value=md_data["data"]["attributes"][
                                        "publicationDemographic"
                                    ],
                                    inline=True,
                                )
                                embedVar.add_field(
                                    name="Status",
                                    value=md_data["data"]["attributes"]["status"],
                                    inline=True,
                                )
                                embedVar.add_field(
                                    name="Last Volume",
                                    value=md_data["data"]["attributes"]["lastVolume"],
                                    inline=True,
                                )
                                embedVar.add_field(
                                    name="Last Chapter",
                                    value=md_data["data"]["attributes"]["lastChapter"],
                                    inline=True,
                                )
                                embedVar.add_field(
                                    name="Tags",
                                    value=str(
                                        [
                                            str(item["attributes"]
                                                ["name"]["en"])
                                            .replace("\n", "")
                                            .replace("'", "")
                                            for item in md_data["data"]["attributes"][
                                                "tags"
                                            ][0:-1]
                                        ]
                                    ),
                                    inline=True,
                                )

                                embedVar.set_image(
                                    url=f"https://uploads.mangadex.org/covers/{id}/{cover_art}"
                                )
                                await ctx.send(embed=embedVar)
                            elif "ja" in data["data"][0]["attributes"]["title"]:
                                embedVar2 = discord.Embed()
                                embedVar2.title = md_data["data"]["attributes"][
                                    "title"
                                ]["ja"]
                                embedVar2.description = (
                                    str(
                                        md_data["data"]["attributes"]["description"][
                                            "ja"
                                        ]
                                    )
                                    .replace("\n", "")
                                    .replace("\r", "")
                                    .replace("'", "")
                                )
                                embedVar2.add_field(
                                    name="Alt Titles",
                                    value=str(
                                        [
                                            title["en"]
                                            for title in md_data["data"]["attributes"][
                                                "altTitles"
                                            ]
                                        ]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Publication Demographics",
                                    value=md_data["data"]["attributes"][
                                        "publicationDemographic"
                                    ],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Status",
                                    value=md_data["data"]["attributes"]["status"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Last Volume",
                                    value=md_data["data"]["attributes"]["lastVolume"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Last Chapter",
                                    value=md_data["data"]["attributes"]["lastChapter"],
                                    inline=True,
                                )
                                embedVar2.add_field(
                                    name="Tags",
                                    value=str(
                                        [
                                            str(item["attributes"]
                                                ["name"]["en"])
                                            .replace("\n", "")
                                            .replace("'", "")
                                            for item in md_data["data"]["attributes"][
                                                "tags"
                                            ][0:-1]
                                        ]
                                    ),
                                    inline=True,
                                )

                                embedVar2.set_image(
                                    url=f"https://uploads.mangadex.org/covers/{id}/{cover_art}"
                                )
                                await ctx.send(embed=embedVar2)

            except Exception as e:
                embedVar = discord.Embed()
                embedVar.description = (
                    "Sadly this command didn't work. Please try again"
                )
                embedVar.add_field(name="Reason", value=e, inline=True)
                await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @manga.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-random", aliases=["md-random"])
    async def manga_random(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get("https://api.mangadex.org/manga/random") as r:
                data = await r.json()
                id = data["data"]["id"]
                cover_art_id = data["data"]["relationships"][2]["id"]
                async with session.get(
                    f"https://api.mangadex.org/cover/{cover_art_id}"
                ) as rp:
                    cover_art_data = await rp.json()
                    cover_art = cover_art_data["data"]["attributes"]["fileName"]
                    try:
                        if r.status == 500:
                            embedError = discord.Embed()
                            embedError.description = (
                                "Sorry, but there was an error. Please try again"
                            )
                            embedError.add_field(
                                name="Reason",
                                value=data["errors"][0]["title"],
                                inline=True,
                            )
                            embedError.add_field(
                                name="Detail",
                                value=data["errors"][0]["detail"],
                                inline=True,
                            )
                            await ctx.send(embed=embedError)
                        else:
                            embedVar = discord.Embed(
                                title=data["data"]["attributes"]["title"]["en"]
                            )
                            embedVar.description = str(
                                data["data"]["attributes"]["description"]["en"]
                            ).replace("\n", "")
                            embedVar.add_field(
                                name="Alt Titles",
                                value=str(
                                    [
                                        title["en"]
                                        for title in data["data"]["attributes"][
                                            "altTitles"
                                        ]
                                    ]
                                ).replace("'", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Original Language",
                                value=str(
                                    [data["data"]["attributes"]
                                        ["originalLanguage"]]
                                ).replace("", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Last Volume",
                                value=str(
                                    [data["data"]["attributes"]["lastVolume"]]
                                ).replace("'", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Last Chapter",
                                value=str(
                                    [data["data"]["attributes"]["lastChapter"]]
                                ).replace("'", ""),
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Publication Demographic",
                                value=data["data"]["attributes"][
                                    "publicationDemographic"
                                ],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Status",
                                value=data["data"]["attributes"]["status"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Content Rating",
                                value=data["data"]["attributes"]["contentRating"],
                                inline=True,
                            )
                            embedVar.add_field(
                                name="Tags",
                                value=str(
                                    [
                                        item["attributes"]["name"]["en"]
                                        for item in data["data"]["attributes"]["tags"][
                                            0:-1
                                        ]
                                    ]
                                )
                                .replace("\n", "")
                                .replace("'", ""),
                                inline=True,
                            )
                            embedVar.set_image(
                                url=f"https://uploads.mangadex.org/covers/{id}/{cover_art}"
                            )
                            await ctx.send(embed=embedVar)
                    except Exception as e:
                        embedVar = discord.Embed()
                        embedVar.description = (
                            f"The query could not be performed. Please try again."
                        )
                        embedVar.add_field(name="Reason", value=e, inline=True)
                        await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @manga_random.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-scanlation-search", aliases=["md-ss"])
    async def scanlation_search(self, ctx, *, search: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {
                "limit": 1,
                "name": search,
                "order[name]": "asc",
                "order[relevance]": "desc",
            }
            async with session.get(
                "https://api.mangadex.org/group", params=params
            ) as totally_another_response:
                md_data2 = await totally_another_response.json()
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
                        await ctx.send(embed=embed1)
                    else:
                        embed2 = discord.Embed()
                        embed2.title = md_data2["data"][0]["attributes"]["name"]
                        embed2.description = md_data2["data"][0]["attributes"][
                            "description"
                        ]
                        embed2.add_field(
                            name="Alt Names",
                            value=md_data2["data"][0]["attributes"]["altNames"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Website",
                            value=str(
                                [md_data2["data"][0]["attributes"]["website"]]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embed2.add_field(
                            name="IRC Server",
                            value=md_data2["data"][0]["attributes"]["ircServer"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Discord",
                            value=f"https://discord.gg/{md_data2['data'][0]['attributes']['discord']}",
                            inline=True,
                        )
                        embed2.add_field(
                            name="Contact Email",
                            value=str(
                                [md_data2["data"][0]["attributes"]["contactEmail"]]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embed2.add_field(
                            name="Twitter",
                            value=md_data2["data"][0]["attributes"]["twitter"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Focused Languages",
                            value=md_data2["data"][0]["attributes"]["focusedLanguages"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Official",
                            value=md_data2["data"][0]["attributes"]["official"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Verified",
                            value=md_data2["data"][0]["attributes"]["verified"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Created At",
                            value=md_data2["data"][0]["attributes"]["createdAt"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Updated At",
                            value=md_data2["data"][0]["attributes"]["updatedAt"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Inactive",
                            value=md_data2["data"][0]["attributes"]["inactive"],
                            inline=True,
                        )
                        await ctx.send(embed=embed2)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @scanlation_search.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV4(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="mangadex-scanlation-id", aliases=["md-si"])
    async def scanlation_id(self, ctx, *, scanlation_id: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.mangadex.org/group/{scanlation_id}"
            ) as another_response:
                payload = await another_response.json()
                try:
                    if payload["data"] is None:
                        embed1 = discord.Embed()
                        embed1.description = (
                            "Sorry, but no results were found... Please try again."
                        )
                        embed1.add_field(
                            name="Total", value=payload["total"], inline=True
                        )
                        embed1.add_field(
                            name="HTTP Status",
                            value=another_response.status,
                            inline=True,
                        )
                        await ctx.send(embed=embed1)
                    else:
                        embed2 = discord.Embed()
                        embed2.title = payload["data"]["attributes"]["name"]
                        embed2.description = payload["data"]["attributes"][
                            "description"
                        ]
                        embed2.add_field(
                            name="Alt Names",
                            value=payload["data"]["attributes"]["altNames"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Website",
                            value=str(
                                [payload["data"]["attributes"]["website"]]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embed2.add_field(
                            name="IRC Server",
                            value=payload["data"]["attributes"]["ircServer"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Discord",
                            value=f"https://discord.gg/{payload['data']['attributes']['discord']}",
                            inline=True,
                        )
                        embed2.add_field(
                            name="Contact Email",
                            value=str(
                                [payload["data"]["attributes"]["contactEmail"]]
                            ).replace("'", ""),
                            inline=True,
                        )
                        embed2.add_field(
                            name="Twitter",
                            value=payload["data"]["attributes"]["twitter"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Focused Languages",
                            value=payload["data"]["attributes"]["focusedLanguages"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Official",
                            value=payload["data"]["attributes"]["official"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Verified",
                            value=payload["data"]["attributes"]["verified"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Created At",
                            value=payload["data"]["attributes"]["createdAt"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Updated At",
                            value=payload["data"]["attributes"]["updatedAt"],
                            inline=True,
                        )
                        embed2.add_field(
                            name="Inactive",
                            value=payload["data"]["attributes"]["inactive"],
                            inline=True,
                        )
                        await ctx.send(embed=embed2)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @scanlation_id.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-user", aliases=["md-user"])
    async def user(self, ctx, *, user_id: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.mangadex.org/user/{user_id}") as rep:
                payload = await rep.json()
                try:
                    embed = discord.Embed()
                    embed.title = payload["data"]["attributes"]["username"]
                    embed.add_field(
                        name="ID", value=payload["data"]["id"], inline=True)
                    embed.add_field(
                        name="Type", value=payload["data"]["type"], inline=True
                    )
                    embed.add_field(
                        name="Roles",
                        value=payload["data"]["attributes"]["roles"],
                        inline=True,
                    )
                    await ctx.send(embed=embed)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @user.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV6(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-author", aliases=["md-author"])
    async def author(self, ctx, *, author_name: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"limit": 1, "name": author_name, "order[name]": "asc"}
            async with session.get(
                "https://api.mangadex.org/author", params=params
            ) as author_response:
                author_payload = await author_response.json()
                try:
                    if author_payload["data"][0]["attributes"]["imageUrl"] is None:
                        embedVar = discord.Embed()
                        embedVar.title = author_payload["data"][0]["attributes"]["name"]
                        embedVar.description = author_payload["data"][0]["attributes"][
                            "biography"
                        ]
                        embedVar.add_field(
                            name="ID",
                            value=author_payload["data"][0]["id"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Twitter",
                            value=author_payload["data"][0]["attributes"]["twitter"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Pixiv",
                            value=author_payload["data"][0]["attributes"]["pixiv"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="MelonBook",
                            value=author_payload["data"][0]["attributes"]["melonBook"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="FanBox",
                            value=author_payload["data"][0]["attributes"]["fanBox"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Booth",
                            value=author_payload["data"][0]["attributes"]["booth"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="NicoVideo",
                            value=author_payload["data"][0]["attributes"]["nicoVideo"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Skeb",
                            value=author_payload["data"][0]["attributes"]["skeb"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Fantia",
                            value=author_payload["data"][0]["id"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Tumblr",
                            value=author_payload["data"][0]["attributes"]["tumblr"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="YouTube",
                            value=author_payload["data"][0]["attributes"]["youtube"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Website",
                            value=author_payload["data"][0]["attributes"]["website"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Created At",
                            value=author_payload["data"][0]["attributes"]["createdAt"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Updated At",
                            value=author_payload["data"][0]["attributes"]["updatedAt"],
                            inline=True,
                        )
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar2 = discord.Embed()
                        embedVar2.title = author_payload["data"][0]["attributes"][
                            "name"
                        ]
                        embedVar2.description = author_payload["data"][0]["attributes"][
                            "biography"
                        ]
                        embedVar2.add_field(
                            name="ID",
                            value=author_payload["data"][0]["id"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Twitter",
                            value=author_payload["data"][0]["attributes"]["twitter"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Pixiv",
                            value=author_payload["data"][0]["attributes"]["pixiv"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="MelonBook",
                            value=author_payload["data"][0]["attributes"]["melonbook"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="FanBox",
                            value=author_payload["data"][0]["attributes"]["fanbox"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Booth",
                            value=author_payload["data"][0]["attributes"]["booth"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="NicoVideo",
                            value=author_payload["data"][0]["attributes"]["nico"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Sekb",
                            value=author_payload["data"][0]["attributes"]["sekb"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Fantia",
                            value=author_payload["data"][0]["id"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Tumblr",
                            value=author_payload["data"][0]["attributes"]["tumblr"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="YouTube",
                            value=author_payload["data"][0]["attributes"]["youtube"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Website",
                            value=author_payload["data"][0]["attributes"]["website"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Created At",
                            value=author_payload["data"][0]["attributes"]["createdAt"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Updated At",
                            value=author_payload["data"][0]["attributes"]["updatedAt"],
                            inline=True,
                        )
                        embedVar2.set_image(
                            url=author_payload["data"][0]["attributes"]["imageUrl"]
                        )
                        await ctx.send(embed=embedVar2)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @author.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexV7(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mangadex-author-id", aliases=["md-author-id"])
    async def author_id(self, ctx, *, author_id: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(
                f"https://api.mangadex.org/author/{author_id}"
            ) as author_r:
                author_data = await author_r.json()
                try:
                    if author_data["data"]["attributes"]["imageUrl"] is None:
                        embedVar = discord.Embed()
                        embedVar.title = author_data["data"]["attributes"]["name"]
                        embedVar.description = author_data["data"]["attributes"][
                            "biography"
                        ]
                        embedVar.add_field(
                            name="ID", value=author_data["data"]["id"], inline=True
                        )
                        embedVar.add_field(
                            name="Twitter",
                            value=author_data["data"]["attributes"]["twitter"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Pixiv",
                            value=author_data["data"]["attributes"]["pixiv"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="MelonBook",
                            value=author_data["data"]["attributes"]["melonBook"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="FanBox",
                            value=author_data["data"]["attributes"]["fanBox"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Booth",
                            value=author_data["data"]["attributes"]["booth"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="NicoVideo",
                            value=author_data["data"]["attributes"]["nicoVideo"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Skeb",
                            value=author_data["data"]["attributes"]["skeb"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Fantia", value=author_data["data"]["id"], inline=True
                        )
                        embedVar.add_field(
                            name="Tumblr",
                            value=author_data["data"]["attributes"]["tumblr"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="YouTube",
                            value=author_data["data"]["attributes"]["youtube"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Website",
                            value=author_data["data"]["attributes"]["website"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Created At",
                            value=author_data["data"]["attributes"]["createdAt"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Updated At",
                            value=author_data["data"]["attributes"]["updatedAt"],
                            inline=True,
                        )
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar2 = discord.Embed()
                        embedVar2.title = author_data["data"]["attributes"]["name"]
                        embedVar2.description = author_data["data"]["attributes"][
                            "biography"
                        ]
                        embedVar2.add_field(
                            name="ID", value=author_data["data"]["id"], inline=True
                        )
                        embedVar2.add_field(
                            name="Twitter",
                            value=author_data["data"]["attributes"]["twitter"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Pixiv",
                            value=author_data["data"]["attributes"]["pixiv"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="MelonBook",
                            value=author_data["data"]["attributes"]["melonbook"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="FanBox",
                            value=author_data["data"]["attributes"]["fanbox"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Booth",
                            value=author_data["data"]["attributes"]["booth"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="NicoVideo",
                            value=author_data["data"]["attributes"]["nico"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Sekb",
                            value=author_data["data"]["attributes"]["sekb"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Fantia", value=author_data["data"]["id"], inline=True
                        )
                        embedVar2.add_field(
                            name="Tumblr",
                            value=author_data["data"]["attributes"]["tumblr"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="YouTube",
                            value=author_data["data"]["attributes"]["youtube"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Website",
                            value=author_data["data"]["attributes"]["website"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Created At",
                            value=author_data["data"]["attributes"]["createdAt"],
                            inline=True,
                        )
                        embedVar2.add_field(
                            name="Updated At",
                            value=author_data["data"]["attributes"]["updatedAt"],
                            inline=True,
                        )
                        embedVar2.set_image(
                            url=author_data["data"]["attributes"]["imageUrl"]
                        )
                        await ctx.send(embed=embedVar2)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = (
                        f"The query could not be performed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @author_id.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class MangaDexReaderV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    bot.add_cog(MangaDexV7(bot))
