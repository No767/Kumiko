import os

import discord
import simdjson
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from rin_exceptions import NoItemsError

load_dotenv()

GITHUB_API_KEY = os.environ["GITHUB_API_KEY"]
REDDIT_ID = os.environ["REDDIT_ID"]
REDDIT_SECRET = os.environ["REDDIT_SECRET"]
TENOR_API_KEY = os.environ["TENOR_API_KEY"]

parser = simdjson.Parser()


class Search(commands.Cog):
    """Search for anime, manga, gifs, memes, and much more!"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    search = SlashCommandGroup("search")
    searchGithub = search.create_subgroup(
        "github", "Search for repos and releases on GitHub"
    )
    searchModrinth = search.create_subgroup(
        "mc-mods", "Search for Minecraft mods and plugins on Modrinth"
    )
    searchGifs = search.create_subgroup("gifs", "Search for GIFs on Tenor")
    searchReddit = search.create_subgroup("reddit", "Search memes and posts on Reddit")

    @search.command(name="anime")
    async def aniListSearchAnime(self, ctx, name: Option(str, "The name of the anime")):
        """Searches up animes"""
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

            params = {"animeName": name, "perPage": 25, "isAdult": False}
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

    @search.command(name="manga")
    async def aniListSearchManga(
        self, ctx, *, name: Option(str, "The name of the manga")
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

            params = {"mangaName": name, "perPage": 25, "isAdult": False}
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


def setup(bot):
    bot.add_cog(Search(bot))
