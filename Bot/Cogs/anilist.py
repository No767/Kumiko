import asyncio

import discord
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from rin_exceptions import NoItemsError


class AniListV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    anilist = SlashCommandGroup("anilist", "Commands for AniList service")
    anilistSearch = anilist.create_subgroup("search", "Search for anime on AniList")

    @anilistSearch.command(name="anime")
    async def aniListSearchAnime(
        self, ctx, *, anime_name: Option(str, "The name of the anime")
    ):
        """Searches for up to 25 animes on AniList"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            query = gql(
                """
            query ($animeName: String!, $perPage: Int, $isAdult: Boolean!) {
                Page (perPage: $perPage){
                    media(search: $animeName, isAdult: $isAdult, type: ANIME) {
                        title {
                            native
                            english
                            romaji
                        }
                        description
                        format
                        status
                        seasonYear
                        startDate {
                            day
                            month
                            year
                        }
                        endDate {
                            day
                            month
                            year
                        }
                        coverImage {
                            extraLarge
                        }
                        genres
                        tags {
                            name
                        }
                        synonyms
                        id
                        
                    }
                }
            }
        """
            )

            params = {"animeName": anime_name, "perPage": 25, "isAdult": False}
            data = await session.execute(query, variable_values=params)
            try:
                if len(data["Page"]["media"]) == 0:
                    raise NoItemsError
                else:
                    mainPages = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=mainItem["title"]["romaji"],
                                description=str(mainItem["description"]).replace(
                                    "<br>", ""
                                ),
                            )
                            .add_field(
                                name="Native Name",
                                value=f'[{mainItem["title"]["native"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="English Name",
                                value=f'[{mainItem["title"]["english"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="Status", value=mainItem["status"], inline=True
                            )
                            .add_field(
                                name="Start Date",
                                value=f'{mainItem["startDate"]["year"]}-{mainItem["startDate"]["month"]}-{mainItem["startDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="End Date",
                                value=f'{mainItem["endDate"]["year"]}-{mainItem["endDate"]["month"]}-{mainItem["endDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="Genres", value=mainItem["genres"], inline=True
                            )
                            .add_field(
                                name="Synonyms", value=mainItem["synonyms"], inline=True
                            )
                            .add_field(
                                name="Format", value=mainItem["format"], inline=True
                            )
                            .add_field(
                                name="Season Year",
                                value=mainItem["seasonYear"],
                                inline=True,
                            )
                            .add_field(
                                name="Tags",
                                value=[tagItem["name"] for tagItem in mainItem["tags"]],
                                inline=True,
                            )
                            .add_field(
                                name="AniList URL",
                                value=f"https://anilist.co/anime/{mainItem['id']}",
                                inline=True,
                            )
                            .set_image(url=mainItem["coverImage"]["extraLarge"])
                            for mainItem in data["Page"]["media"]
                        ],
                        loop_pages=True,
                    )
                    await mainPages.respond(ctx.interaction, ephemeral=False)
            except NoItemsError:
                embedNoItemsError = discord.Embed()
                embedNoItemsError.description = "Sorry, but there seems to be no anime(s) with that name. Please try again"
                await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @anilistSearch.command(name="manga")
    async def aniListSearchManga(
        self, ctx, *, manga_name: Option(str, "The name of the manga")
    ):
        """Searches for up to 25 mangas on AniList"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            query = gql(
                """
            query ($mangaName: String!, $perPage: Int, $isAdult: Boolean!) {
                Page (perPage: $perPage){
                    media(search: $mangaName, isAdult: $isAdult, type: MANGA) {
                        title {
                            native
                            english
                            romaji
                        }
                        description
                        format
                        status
                        startDate {
                            day
                            month
                            year
                        }
                        endDate {
                            day
                            month
                            year
                        }
                        coverImage {
                            extraLarge
                        }
                        genres
                        tags {
                            name
                        }
                        synonyms
                        id
                        
                    }
                }
            }
        """
            )

            params = {"mangaName": manga_name, "perPage": 25, "isAdult": False}
            data = await session.execute(query, variable_values=params)
            try:
                if len(data["Page"]["media"]) == 0:
                    raise NoItemsError
                else:
                    mainPages2 = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=mainItem["title"]["romaji"],
                                description=str(mainItem["description"]).replace(
                                    "<br>", ""
                                ),
                            )
                            .add_field(
                                name="Native Name",
                                value=f'[{mainItem["title"]["native"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="English Name",
                                value=f'[{mainItem["title"]["english"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="Status", value=mainItem["status"], inline=True
                            )
                            .add_field(
                                name="Start Date",
                                value=f'{mainItem["startDate"]["year"]}-{mainItem["startDate"]["month"]}-{mainItem["startDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="End Date",
                                value=f'{mainItem["endDate"]["year"]}-{mainItem["endDate"]["month"]}-{mainItem["endDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="Genres", value=mainItem["genres"], inline=True
                            )
                            .add_field(
                                name="Synonyms", value=mainItem["synonyms"], inline=True
                            )
                            .add_field(
                                name="Format", value=mainItem["format"], inline=True
                            )
                            .add_field(
                                name="Tags",
                                value=[tagItem["name"] for tagItem in mainItem["tags"]],
                                inline=True,
                            )
                            .add_field(
                                name="AniList URL",
                                value=f"https://anilist.co/manga/{mainItem['id']}",
                                inline=True,
                            )
                            .set_image(url=mainItem["coverImage"]["extraLarge"])
                            for mainItem in data["Page"]["media"]
                        ],
                        loop_pages=True,
                    )

                    await mainPages2.respond(ctx.interaction, ephemeral=False)
            except NoItemsError:
                embedNoItemsError = discord.Embed()
                embedNoItemsError.description = "Sorry, but there seems to be no manga(s) with that name. Please try again"
                await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @anilistSearch.command(name="tags")
    async def aniListSearchTags(
        self, ctx, *, tags: Option(str, "The name of the tag to search for")
    ):
        """Searches up to 25 animes and mangas based on the given tag"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            query = gql(
                """
            query ($tagName: String!, $perPage: Int, $isAdult: Boolean!) {
                Page (perPage: $perPage){
                    media(tag: $tagName, isAdult: $isAdult) {
                        title {
                            native
                            english
                            romaji
                        }
                        description
                        format
                        status
                        startDate {
                            day
                            month
                            year
                        }
                        endDate {
                            day
                            month
                            year
                        }
                        coverImage {
                            extraLarge
                        }
                        genres
                        type
                        tags {
                            name
                        }
                        synonyms
                        id
                    }
                }
            }
        """
            )

            params = {"tagName": tags, "perPage": 25, "isAdult": False}
            data = await session.execute(query, variable_values=params)
            try:
                if len(data["Page"]["media"]) == 0:
                    raise NoItemsError
                else:
                    mainPages2 = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=mainItem["title"]["romaji"],
                                description=str(mainItem["description"]).replace(
                                    "<br>", ""
                                ),
                            )
                            .add_field(
                                name="Native Name",
                                value=f'[{mainItem["title"]["native"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="English Name",
                                value=f'[{mainItem["title"]["english"]}]',
                                inline=True,
                            )
                            .add_field(
                                name="Status", value=mainItem["status"], inline=True
                            )
                            .add_field(
                                name="Start Date",
                                value=f'{mainItem["startDate"]["year"]}-{mainItem["startDate"]["month"]}-{mainItem["startDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="End Date",
                                value=f'{mainItem["endDate"]["year"]}-{mainItem["endDate"]["month"]}-{mainItem["endDate"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="Genres", value=mainItem["genres"], inline=True
                            )
                            .add_field(
                                name="Synonyms", value=mainItem["synonyms"], inline=True
                            )
                            .add_field(
                                name="Format", value=mainItem["format"], inline=True
                            )
                            .add_field(name="Type", value=mainItem["type"], inline=True)
                            .add_field(
                                name="Tags",
                                value=[tagItem["name"] for tagItem in mainItem["tags"]],
                                inline=True,
                            )
                            .add_field(
                                name="AniList URL",
                                value=f"https://anilist.co/anime/{mainItem['id']}"
                                if str(mainItem["type"]) == "ANIME"
                                else f"https://anilist.co/manga/{mainItem['id']}",
                                inline=True,
                            )
                            .set_image(url=mainItem["coverImage"]["extraLarge"])
                            for mainItem in data["Page"]["media"]
                        ],
                        loop_pages=True,
                    )

                    await mainPages2.respond(ctx.interaction, ephemeral=False)
            except NoItemsError:
                embedNoItemsError = discord.Embed()
                embedNoItemsError.description = "Sorry, but there seems to be no tag with that name. Please try again"
                await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @anilistSearch.command(name="users")
    async def anilistSearchUsers(
        self, ctx, *, user: Option(str, "The user to search for")
    ):
        """Provides up to 25 users from the given username"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            mainQuery = gql(
                """ 
                query ($name: String!, $perPage: Int) {
                    Page (perPage: $perPage) {
                        users (name: $name) {
                            name
                            about
                            avatar {
                                large
                            }
                            siteUrl
                            statistics {
                                anime {
                                    count
                                    meanScore
                                    minutesWatched
                                    episodesWatched
                                }
                                manga {
                                    count
                                    meanScore
                                    minutesWatched
                                    chaptersRead
                                    volumesRead
                                }
                            }
                        }
                    }
                }
                """
            )
            params = {"name": user, "perPage": 25}
            data = await session.execute(mainQuery, variable_values=params)
            try:
                if len(data["Page"]["users"]) == 0:
                    raise NoItemsError
                else:
                    mainPages3 = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=dictItem["name"], description=dictItem["about"]
                            )
                            .add_field(
                                name="Site URL", value=dictItem["siteUrl"], inline=True
                            )
                            .add_field(
                                name="Animes Watched",
                                value=dictItem["statistics"]["anime"]["count"],
                                inline=True,
                            )
                            .add_field(
                                name="Anime Mean Score",
                                value=dictItem["statistics"]["anime"]["meanScore"],
                                inline=True,
                            )
                            .add_field(
                                name="Minutes Watched",
                                value=dictItem["statistics"]["anime"]["minutesWatched"],
                                inline=True,
                            )
                            .add_field(
                                name="Mangas Read",
                                value=dictItem["statistics"]["manga"]["count"],
                                inline=True,
                            )
                            .add_field(
                                name="Minutes Watched",
                                value=dictItem["statistics"]["manga"]["minutesWatched"],
                                inline=True,
                            )
                            .add_field(
                                name="Chapters Read",
                                value=dictItem["statistics"]["manga"]["chaptersRead"],
                                inline=True,
                            )
                            .add_field(
                                name="Volumes Read",
                                value=dictItem["statistics"]["manga"]["volumesRead"],
                                inline=True,
                            )
                            .set_thumbnail(url=dictItem["avatar"]["large"])
                            for dictItem in data["Page"]["users"]
                        ],
                        loop_pages=True,
                    )
                    await mainPages3.respond(ctx.interaction, ephemeral=False)
            except NoItemsError:
                embedNoItemsError = discord.Embed()
                embedNoItemsError.description = "Sorry, but there seems to be no users with that name. Please try again"
                await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @anilistSearch.command(name="characters")
    async def aniListSearchCharacter(
        self, ctx, *, anime_character: Option(str, "The character to search for")
    ):
        """Searches up to 25 anime characters on AniList"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            mainQuery = gql(
                """ 
                query ($search: String!, $perPage: Int) {
                    Page (perPage: $perPage) {
                        characters (search: $search) {
                            name {
                                full
                                native
                                alternative
                            }
                            description
                            image {
                                large
                            }
                            gender
                            age
                            media {
                                nodes {
                                    title {
                                        romaji
                                    }
                                }
                            }
                            id

                        }
                    }
                }
                """
            )
            params = {"search": anime_character, "perPage": 25}
            data = await session.execute(mainQuery, variable_values=params)
            try:
                if len(data["Page"]["characters"]) == 0:
                    raise NoItemsError
                else:
                    pagesMain2 = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=f'{mainItem3["name"]["full"]} - {mainItem3["name"]["native"]}',
                                description=mainItem3["description"],
                            )
                            .add_field(
                                name="Alternative Name",
                                value=str(mainItem3["name"]["alternative"]).replace(
                                    "'", ""
                                ),
                                inline=True,
                            )
                            .add_field(
                                name="Gender", value=mainItem3["gender"], inline=True
                            )
                            .add_field(name="Age", value=mainItem3["age"], inline=True)
                            .add_field(
                                name="Media",
                                value=str(
                                    [
                                        mediaMain["title"]["romaji"]
                                        for mediaMain in mainItem3["media"]["nodes"]
                                    ]
                                ).replace("'", ""),
                            )
                            .add_field(
                                name="AniList URL",
                                value=f"https://anilist.co/character/{mainItem3['id']}",
                                inline=True,
                            )
                            .set_image(url=mainItem3["image"]["large"])
                            for mainItem3 in data["Page"]["characters"]
                        ],
                        loop_pages=True,
                    )
                    await pagesMain2.respond(ctx.interaction, ephemeral=False)
            except NoItemsError:
                embedNoItemsError = discord.Embed()
                embedNoItemsError.description = "Sorry, but there seems to be no anime and/or manga characters with that name. Please try again"
                await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @anilistSearch.command(name="actors")
    async def aniListSearchStaff(
        self, ctx, *, voice_actor: Option(str, "The voice actor of the character")
    ):
        """Searches for up to 25 voice actors or staff that have worked on an anime and/or its characters"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            mainQuery = gql(
                """ 
                query ($search: String!, $perPage: Int) {
                    Page (perPage: $perPage) {
                        staff (search: $search) {
                            name {
                                full
                                native
                            }
                            description
                            languageV2
                            image {
                                large
                            }
                            gender
                            dateOfBirth {
                                year
                                month
                                day
                            }
                            dateOfDeath {
                                year
                                month
                                day
                            }
                            age
                            yearsActive
                            homeTown
                            characters {
                                nodes {
                                    name {
                                        full
                                    }
                                }
                            }
                            id
                        }
                    }
                }
                """
            )
            params = {"search": voice_actor, "perPage": 25}
            data = await session.execute(mainQuery, variable_values=params)
            try:
                if len(data["Page"]["staff"]) == 0:
                    raise NoItemsError
                else:
                    pagesMain3 = pages.Paginator(
                        pages=[
                            discord.Embed(
                                title=f'{mainItem5["name"]["full"]} - {mainItem5["name"]["native"]}',
                                description=mainItem5["description"],
                            )
                            .add_field(
                                name="Primary Language",
                                value=mainItem5["languageV2"],
                                inline=True,
                            )
                            .add_field(
                                name="Gender", value=mainItem5["gender"], inline=True
                            )
                            .add_field(name="Age", value=mainItem5["age"], inline=True)
                            .add_field(
                                name="Hometown",
                                value=mainItem5["homeTown"],
                                inline=True,
                            )
                            .add_field(
                                name="Years Active",
                                value=mainItem5["yearsActive"],
                                inline=True,
                            )
                            .add_field(
                                name="Date of Birth",
                                value=f'{mainItem5["dateOfBirth"]["year"]}-{mainItem5["dateOfBirth"]["year"]}-{mainItem5["dateOfBirth"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="Date of Death",
                                value=f'{mainItem5["dateOfDeath"]["year"]}-{mainItem5["dateOfDeath"]["year"]}-{mainItem5["dateOfDeath"]["day"]}',
                                inline=True,
                            )
                            .add_field(
                                name="Characters",
                                value=str(
                                    [
                                        characterName["name"]["full"]
                                        for characterName in mainItem5["characters"][
                                            "nodes"
                                        ]
                                    ]
                                ).replace("'", ""),
                                inline=True,
                            )
                            .add_field(
                                name="AniList URL",
                                value=f"https://anilist.co/staff/{mainItem5['id']}",
                                inline=True,
                            )
                            .set_image(url=mainItem5["image"]["large"])
                            for mainItem5 in data["Page"]["staff"]
                        ],
                        loop_pages=True,
                    )
                    await pagesMain3.respond(ctx.interaction, ephemeral=False)
            except NoItemsError:
                embedNoItemsError = discord.Embed()
                embedNoItemsError.description = "Sorry, but there seems to be no staff and/or voice actors with that name. Please try again"
                await ctx.respond(embed=embedNoItemsError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(AniListV1(bot))
