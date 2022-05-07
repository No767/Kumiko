import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands

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
                sensesFilter = [
                    "restrictions",
                    "english_definitions",
                    "sentences",
                    "links",
                ]
                try:
                    if len(jishoMain["data"]) == 0:
                        raise ValueError
                    else:

                        embedVar = discord.Embed()
                        for dictItem in jishoMain["data"]:
                            for jpnItem in dictItem["japanese"]:
                                totalJpnItem = [value for _,
                                                value in jpnItem.items()]
                            for itemVal in dictItem["senses"]:
                                for keys, value in itemVal.items():
                                    if keys not in engDefFilter:
                                        valueItem = value
                            for valOfItem in dictItem["senses"]:
                                for (
                                    item3,
                                    res3,
                                ) in valOfItem.items():
                                    if item3 not in sensesFilter:
                                        embedVar.insert_field_at(
                                            index=1,
                                            name=item3,
                                            value=str(res3).replace("'", ""),
                                            inline=True,
                                        )
                                        embedVar.remove_field(6)

                            embedVar.title = (
                                str(totalJpnItem)
                                .replace("'", "")
                                .replace("[", "")
                                .replace("]", "")
                            )
                            embedVar.description = (
                                str(valueItem)
                                .replace("'", "")
                                .replace("[", "")
                                .replace("]", "")
                            )
                            await ctx.respond(embed=embedVar)
                except ValueError:
                    embedValError = discord.Embed()
                    embedValError.description = f"It seems like the word `{search}` is not in the dictionary. Please try again."
                    await ctx.respond(embed=embedValError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(jishoDict(bot))
