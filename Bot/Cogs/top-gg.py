import asyncio
import os

import aiohttp
import discord
import orjson
import uvloop
from discord.commands import Option, slash_command
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("Top_GG_API_Key")


class TopGGV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="topgg-search",
        description="Returns Info about the given Discord bot on Top.gg",
    )
    async def topgg_search_one(self, ctx, bot_id: Option(str, "Discord Bot ID")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            async with session.get(
                f"https://top.gg/api/bots/{bot_id}", headers=headers
            ) as r:
                getOneBotInfo = await r.content.read()
                getOneBotInfoMain = orjson.loads(getOneBotInfo)
                try:
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
                                name=key, value=str(val).replace("'", ""), inline=True
                            )
                    await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(231, 74, 255))
                    embedVar.description = f"The query failed. Please try again."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TopGGV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="topgg-search-users",
        description="Returns Info about the given user on Top.gg",
    )
    async def topgg_search_users(self, ctx, *, user_id: Option(str, "User ID")):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            async with session.get(
                f"https://top.gg/api/users/{user_id}", headers=headers
            ) as response:
                user = await response.content.read()
                userMain = orjson.loads(user)
                try:
                    if "error" in userMain:
                        embed = discord.Embed()
                        embed.description = (
                            "Sorry, but the user could not be found. Please try again"
                        )
                        embed.set_footer(
                            text="Tip: Try finding a user on the Top.gg Disord Server"
                        )
                        embed.add_field(
                            name="Reason", value=userMain["error"], inline=True
                        )
                        await ctx.respond(embed=embed)
                    else:
                        embedVar = discord.Embed(
                            title=userMain["username"],
                            color=discord.Color.from_rgb(191, 242, 255),
                        )
                        embedVar.description = userMain["bio"]
                        excludedKeys = {"bio"}
                        for key, val in userMain.items():
                            if key not in excludedKeys:
                                embedVar.add_field(
                                    name=key, value=val, inline=True)

                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(231, 74, 255))
                    embedVar.description = f"The query failed. Please try again."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(TopGGV1(bot))
    bot.add_cog(TopGGV2(bot))
