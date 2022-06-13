import asyncio

import discord
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from exceptions import NoItemsError
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


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
                    print(data)
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

    @anilist.command(name="recommendations")
    async def aniListRecommendations(
        self, ctx, *, media_id: Option(int, "The ID of the anime/manga")
    ):
        """Returns up to 25 recommendations for an anime or manga"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            mainQuery = gql(
                """ 
                query ($mediaId: Int!, $perPage: Int) {
                    Page (perPage: $perPage) {
                        recommendations (mediaId: $mediaId) {
                            rating
                            mediaRecommendation {
                                title {
                                romaji 
                                native
                            }
                            description 
                            type 
                            startDate {
                                year
                                month
                                day
                            }
                            endDate {
                                year
                                month
                                day
                            }
                            coverImage {
                                extraLarge
                            }
                            genres
                            tags {
                                name
                            }
                            }
                            
                            
                        }
                        
                    }
                }
                """
            )
            try:
                params = {"mediaId": media_id, "perPage": 25}
                data = await session.execute(mainQuery, variable_values=params)
                try:
                    if len(data["Page"]["recommendations"]) == 0:
                        raise NoItemsError
                    else:
                        mainDataPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=f'{item["mediaRecommendation"]["title"]["romaji"]} - {item["mediaRecommendation"]["title"]["native"]}',
                                    description=item["mediaRecommendation"][
                                        "description"
                                    ],
                                )
                                .add_field(
                                    name="Type",
                                    value=item["mediaRecommendation"]["type"],
                                )
                                .add_field(
                                    name="Start Date",
                                    value=f'{item["mediaRecommendation"]["startDate"]["year"]}-{item["mediaRecommendation"]["startDate"]["month"]}-{item["mediaRecommendation"]["startDate"]["day"]}',
                                    inline=True,
                                )
                                .add_field(
                                    name="End Date",
                                    value=f'{item["mediaRecommendation"]["endDate"]["year"]}-{item["mediaRecommendation"]["endDate"]["month"]}-{item["mediaRecommendation"]["endDate"]["day"]}',
                                    inline=True,
                                )
                                .add_field(
                                    name="Genres",
                                    value=str(
                                        item["mediaRecommendation"]["genres"]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="Tags",
                                    value=str(
                                        [
                                            tagsItem["name"]
                                            for tagsItem in item["mediaRecommendation"][
                                                "tags"
                                            ]
                                        ]
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .set_image(
                                    url=item["mediaRecommendation"]["coverImage"][
                                        "extraLarge"
                                    ]
                                )
                                for item in data["Page"]["recommendations"]
                            ],
                            loop_pages=True,
                        )
                        await mainDataPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedNoItemsError = discord.Embed()
                    embedNoItemsError.description = "Sorry, but there seems to be no recommendations for that media. Please try again"
                    await ctx.respond(embed=embedNoItemsError)
            except Exception as e:
                await ctx.respond(
                    discord.Embed(
                        description="Oops, something went wrong. Please try again"
                    ).add_field(name="Error", value=e, inline=True)
                )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @anilist.command(name="reviews")
    async def aniListReviews(
        self, ctx, *, media_id: Option(int, "The ID of the anime/manga")
    ):
        """Returns up to 25 reviews of the given anime/manga ID"""
        transport = AIOHTTPTransport(url="https://graphql.anilist.co/")
        async with Client(
            transport=transport,
            fetch_schema_from_transport=True,
        ) as session:
            mainQuery = gql(
                """ 
                query ($mediaId: Int!, $perPage: Int) {
                    Page (perPage: $perPage) {
                        reviews (mediaId: $mediaId, sort: CREATED_AT_DESC) {
                            body
                            rating
                            ratingAmount
                            score
                            user {
                                name
                                avatar {
                                    large
                                }
                            }
                            media {
                                title {
                                    romaji
                                    native
                                }
                            }
                        }
                    }
                }
                """
            )
            try:
                params = {"mediaId": media_id, "perPage": 25}
                data = await session.execute(mainQuery, variable_values=params)
                try:
                    if len(data["Page"]["reviews"]) == 0:
                        raise NoItemsError
                    else:
                        mainPagesReview = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=f'{reviewItem["media"]["title"]["romaji"]}/{reviewItem["media"]["title"]["native"]}- {reviewItem["user"]["name"]}',
                                    description=reviewItem["body"],
                                )
                                .add_field(
                                    name="Rating",
                                    value=reviewItem["rating"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Rating Amount",
                                    value=reviewItem["ratingAmount"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Score", value=reviewItem["score"], inline=True
                                )
                                .set_thumbnail(
                                    url=reviewItem["user"]["avatar"]["large"]
                                )
                                for reviewItem in data["Pages"]["reviews"]
                            ],
                            loop_pages=True,
                        )
                        await mainPagesReview.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedNoItemsError = discord.Embed()
                    embedNoItemsError.description = "Sorry, but there seems to be no reviews associated with that media. Please try again"
                    await ctx.respond(embed=embedNoItemsError)
            except Exception as e:
                await ctx.respond(
                    discord.Embed(
                        description="Oops, something went wrong. Please try again"
                    ).add_field(name="Error", value=e, inline=True)
                )

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(AniListV1(bot))
