import asyncio
import os

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from dotenv import load_dotenv
from exceptions import NoItemsError

load_dotenv()

apiKey = os.getenv("Top_GG_API_Key")
parser = simdjson.Parser()


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
                getOneBotInfoMain = parser.parse(getOneBotInfo, recursive=True)
                try:
                    try:
                        if "error" in getOneBotInfoMain:
                            raise NoItemsError
                        else:
                            embedVar = discord.Embed(
                                title=getOneBotInfoMain["username"],
                                color=discord.Color.from_rgb(191, 242, 255),
                            )
                            embedVar.description = (
                                str(getOneBotInfoMain["longdesc"])
                                .replace("\r", "")
                                .replace("<div align=center>", "")
                                .replace("<div align=left>", "")
                                .replace("<div align=right>", "")
                            )
                            excludedKeys = {"longdesc", "lib"}
                            for key, val in getOneBotInfoMain.items():
                                if key not in excludedKeys:
                                    embedVar.add_field(
                                        name=key,
                                        value=str(val).replace("'", ""),
                                        inline=True,
                                    )
                            await ctx.respond(embed=embedVar)
                    except NoItemsError:
                        embedError = discord.Embed(
                            color=discord.Color.from_rgb(231, 74, 255)
                        )
                        embedError.description = (
                            "Sorry, but that bot doesn't exist. So please try again..."
                        )
                        await ctx.respond(embed=embedError)
                except Exception as e:
                    embedVar = discord.Embed(color=discord.Color.from_rgb(231, 74, 255))
                    embedVar.description = f"The query failed. Please try again."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(TopGGV1(bot))
