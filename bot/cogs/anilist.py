from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Callable, Literal, Optional

import discord
import msgspec
from discord.ext import commands

if TYPE_CHECKING:
    from libs.utils.context import GuildContext

    from bot.kumiko import Kumiko

import aiohttp
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

### Command Flags


class SearchFlags(commands.FlagConverter):
    title: Annotated[Optional[str], commands.clean_content] = commands.flag(
        name="title", description="The title to search against", default=None
    )

    # Sorting

    sort: Optional[
        Literal[
            "ROLE",
            "ROLE_DESC",
            "SEARCH_MATCH",
            "FAVOURITES",
            "FAVOURITES_DESC",
            "RELEVANCE",
        ]
    ] = commands.flag(
        name="character-sort",
        description="How character information is sorted",
        default="RELEVANCE",
    )

    # Tags

    # This flag probably would work best with an autocomplete
    # these also would work pretty well for autocompletes
    tags: Optional[str] = commands.flag(
        name="tags", description="Tags to specify", default=None
    )
    genre: Optional[
        Literal[
            "Action",
            "Adventure",
            "Comedy",
            "Drama",
            "Ecchi",
            "Fantasy",
            "Horror",
            "Mahou Shoujo",
            "Meecha",
            "Music",
            "Mystery",
            "Psychological",
            "Romance",
            "Sci-Fi",
            "Slice of Life",
            "Sports",
            "Supernatural",
            "Thriller",
        ]
    ] = commands.flag(name="genre", description="Genres to select", default=None)

    # Others
    adult: Optional[bool] = commands.flag(
        name="Whether to include adult related content", default=False
    )


### Transport Overrides


# This is necessary in order to force GQL to see an aiohttp.ClientSession instance
class AIOHTTPTransportExistingSession(AIOHTTPTransport):
    def __init__(
        self, session: aiohttp.ClientSession, deserializer: Callable, *args, **kwargs
    ):
        super().__init__(json_deserialize=deserializer, *args, **kwargs)
        self.session = session

    async def connect(self) -> None:
        pass

    async def close(self) -> None:
        pass


class Anilist(commands.GroupCog):
    """AniList related commands"""

    BASE_URL = "https://graphql.anilist.co/"

    def __init__(self, bot: Kumiko):
        self.bot = bot

        self._transport = AIOHTTPTransportExistingSession(
            session=self.bot.session,
            deserializer=msgspec.json.Decoder,
            url=self.BASE_URL,
        )
        self.client = Client(transport=self._transport)

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:SillyMe:1311606523872411648>")

    @commands.hybrid_command(name="search")
    async def search(self, ctx: GuildContext, *, flags: SearchFlags) -> None:
        await ctx.defer()
        params = {
            "search": flags.title,
            "sort": flags.sort,
            "tagIn": flags.tags,
            "genreIn": flags.genre,
            "isAdult": flags.adult,
        }
        query = gql(
            """
query ($search: String!, $sort: [CharacterSort], $tagIn: [String], $genreIn: [String], $isAdult: Boolean)  {
  Page {
    media (search: $search, tag_in: $tagIn, genre_in: $genreIn, isAdult: $isAdult) {
      id
      title {
        native
        romaji
        english
      }
      description
      chapters
      volumes
      rankings {
        context
        rank
        year
      }
      format
      status
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
      seasonYear
      season
      averageScore
      meanScore
      popularity
      favourites
      studios {
        nodes {
          name
          siteUrl
        }
      }
      hashtag
      genres
      characters(sort: $sort) {
        edges {
          name
          role
          node {
            siteUrl
            image {
              large
            }
          }
        }
      }
      tags {
        category
        isGeneralSpoiler
        isMediaSpoiler
        name
        rank
      }
      coverImage {
        large
      }
    }
  }
}
            """
        )
        async with self.client as session:
            data = await session.execute(query, variable_values=params)
            print(data["Page"])
            await ctx.send("it works")


async def setup(bot: Kumiko) -> None:
    await bot.add_cog(Anilist(bot))
