import asyncio

import aiohttp
import discord
import orjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands


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
                jishoMain = orjson.loads(jisho)
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
                    embedVar = discord.Embed()
                    for dictItem in jishoMain["data"]:
                        for jpnItem in dictItem["japanese"]:
                            totalJpnItem = [value for keys,
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
                except Exception as e:
                    embedError = discord.Embed()
                    embedError.description = (
                        "There was an error with your search. Please try again"
                    )
                    embedError.add_field(name="Error", value=e, inline=True)
                    embedError.add_field(
                        name="HTTP Status Code", value=jisho.status, inline=True
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(jishoDict(bot))
