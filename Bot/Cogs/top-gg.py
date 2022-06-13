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
    async def topgg_search_one(self, ctx, bot_id: Option(str, "Discord Bot ID")):
        """Returns info about the given Discord bot on Top.gg"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            async with session.get(
                f"https://top.gg/api/bots/{bot_id}", headers=headers
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

    @topggSearch.command(name="user")
    async def topgg_search_users(self, ctx, *, user_id: Option(str, "User ID")):
        """Returns info about the given user on Top.gg"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            async with session.get(
                f"https://top.gg/api/users/{user_id}", headers=headers
            ) as response:
                user = await response.content.read()
                userMain = parser.parse(user, recursive=True)
                try:
                    try:
                        if "error" in userMain:
                            raise NoItemsError
                        else:
                            embedVar = discord.Embed(
                                title=userMain["username"],
                                color=discord.Color.from_rgb(191, 242, 255),
                            )
                            embedVar.description = userMain["bio"]
                            excludedKeys = {"bio"}
                            for key, val in userMain.items():
                                if key not in excludedKeys:
                                    embedVar.add_field(name=key, value=val, inline=True)

                            await ctx.respond(embed=embedVar)
                    except NoItemsError:
                        embedError = discord.Embed()
                        embedError.description = (
                            "Sorry, but the user could not be found. Please try again"
                        )
                        embedError.set_footer(
                            text="Tip: Try finding a user on the Top.gg Disord Server"
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
