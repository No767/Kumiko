import asyncio
import os

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("Top_GG_API_Key")


class TopGGV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="topgg-search")
    async def topgg_search_one(self, ctx, *, search: int):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            async with session.get(
                f"https://top.gg/api/bots/{search}", headers=headers
            ) as r:
                getOneBotInfo = await r.json()
                try:
                    embedVar = discord.Embed(
                        title=getOneBotInfo["username"],
                        color=discord.Color.from_rgb(191, 242, 255),
                    )
                    embedVar.description = (
                        str(getOneBotInfo["longdesc"])
                        .replace("\r", "")
                        .replace("<div align=center>", "")
                        .replace("<div align=left>", "")
                        .replace("<div align=right>", "")
                    )
                    excludedKeys = {"longdesc", "lib"}
                    for key, val in getOneBotInfo.items():
                        if key not in excludedKeys:
                            embedVar.add_field(
                                name=key, value=str(val).replace("'", ""), inline=True
                            )
                    await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(231, 74, 255))
                    embedVar.description = (
                        f"The query failed. Please try again.\nReason: {e}"
                    )
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @topgg_search_one.error
    async def on_message(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TopGGV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="topgg-search-users")
    async def topgg_search_users(self, ctx, *, search: int):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            async with session.get(
                f"https://top.gg/api/users/{search}", headers=headers
            ) as response:
                user = await response.json()
                try:
                    if "error" in user:
                        embed = discord.Embed()
                        embed.description = (
                            "Sorry, but the user could not be found. Please try again"
                        )
                        embed.set_footer(
                            text="Tip: Try finding a user on the Top.gg Disord Server"
                        )
                        embed.add_field(
                            name="Reason", value=user["error"], inline=True)
                        await ctx.send(embed=embed)
                    else:
                        embedVar = discord.Embed(
                            title=user["username"],
                            color=discord.Color.from_rgb(191, 242, 255),
                        )
                        embedVar.description = user["bio"]
                        excludedKeys = {"bio"}
                        for key, val in user.items():
                            if key not in excludedKeys:
                                embedVar.add_field(
                                    name=key, value=val, inline=True)

                        await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(
                        color=discord.Color.from_rgb(231, 74, 255))
                    embedVar.description = (
                        f"The query failed. Please try again.\nReason: {e}"
                    )
                    await ctx.send(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @topgg_search_users.error
    async def on_message(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(TopGGV1(bot))
    bot.add_cog(TopGGV2(bot))
