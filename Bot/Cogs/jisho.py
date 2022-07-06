import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands, pages

parser = simdjson.Parser()


class jishoDict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="jisho",
        description="Searches for words on Jisho",
    )
    async def jishoSearcher(
        self,
        ctx,
        search: Option(
            str,
            "The word you want to search for. It could be in either English or Japanese.",
        ),
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"keyword": search}
            async with session.get(
                "https://jisho.org/api/v1/search/words", params=params
            ) as r:
                jisho = await r.content.read()
                jishoMain = parser.parse(jisho, recursive=True)
                engDefFilter = [
                    "parts_of_speech",
                    "links",
                    "tags",
                    "restrictions",
                    "see_also",
                    "antonyms",
                    "source",
                    "info",
                    "sentences",
                ]
                try:
                    if len(jishoMain["data"]) == 0:
                        raise ValueError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=str(
                                        next(
                                            [value for _, value in jpnItem.items()]
                                            for jpnItem in dictItem["japanese"]
                                        )
                                    )
                                    .replace("'", "")
                                    .replace("[", "")
                                    .replace("]", ""),
                                    description=str(
                                        [
                                            v
                                            for itemVal in dictItem["senses"]
                                            for k, v, in itemVal.items()
                                            if k not in engDefFilter
                                        ]
                                    )
                                    .replace("[", "")
                                    .replace("]", "")
                                    .replace("'", ""),
                                )
                                .add_field(
                                    name="Parts of Speech",
                                    value=str(
                                        next(
                                            (
                                                mainItem["parts_of_speech"]
                                                for mainItem in dictItem["senses"]
                                            )
                                        )
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="Tags",
                                    value=str(
                                        next(
                                            (
                                                mainItem["tags"]
                                                for mainItem in dictItem["senses"]
                                            )
                                        )
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                .add_field(
                                    name="See Also",
                                    value=str(
                                        next(
                                            (
                                                mainItem["see_also"]
                                                for mainItem in dictItem["senses"]
                                            )
                                        )
                                    ).replace("'", ""),
                                    inline=True,
                                )
                                for dictItem in jishoMain["data"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except ValueError:
                    embedValError = discord.Embed()
                    embedValError.description = f"It seems like the word `{search}` is not in the dictionary. Please try again."
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(jishoDict(bot))
