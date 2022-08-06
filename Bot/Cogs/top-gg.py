import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from rin_exceptions import NoItemsError

load_dotenv()

apiKey = os.getenv("Top_GG_API_Key")
jsonParser = simdjson.Parser()


class TopGGV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    topgg = SlashCommandGroup("topgg", "Commands for Top.gg")
    topggSearch = topgg.create_subgroup("search", "Searches for an item on Top.gg")

    @topggSearch.command(name="bot")
    async def topgg_search_one(
        self, ctx, search_query: Option(str, "The name of the bot")
    ):
        """Searches up to 25 bots on Top.gg"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            params = {"search": search_query, "limit": 25}
            async with session.get(
                "https://top.gg/api/bots", headers=headers, params=params
            ) as r:
                getOneBotInfo = await r.content.read()
                getOneBotInfoMain = jsonParser.parse(getOneBotInfo, recursive=True)
                try:
                    if "error" in getOneBotInfoMain:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=mainItem["username"],
                                    description=mainItem["shortdesc"],
                                )
                                .add_field(
                                    name="Invite", value=mainItem["invite"], inline=True
                                )
                                .add_field(
                                    name="Website",
                                    value=f"[{mainItem['website']}]",
                                    inline=True,
                                )
                                .add_field(
                                    name="Prefix", value=mainItem["prefix"], inline=True
                                )
                                .add_field(
                                    name="Date Added",
                                    value=parser.isoparse(mainItem["date"]).strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                    inline=True,
                                )
                                for mainItem in getOneBotInfoMain["results"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedError = discord.Embed(
                        color=discord.Color.from_rgb(231, 74, 255)
                    )
                    embedError.description = (
                        "Sorry, but that bot doesn't exist. So please try again..."
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(TopGGV1(bot))
