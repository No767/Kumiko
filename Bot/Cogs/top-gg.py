import os

import aiohttp
import discord
import orjson
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import uvloop

load_dotenv()

key = os.getenv("Top_GG_API_Key")


class TopGGV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="topgg-search")
    async def topgg_search_one(self, ctx, *, search: int):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": key}
            async with session.get(
                f"https://top.gg/api/bots/{search}", headers=headers
            ) as r:
                getOneBotInfo = await r.json()
                try:
                    embedVar = discord.Embed(
                        title=getOneBotInfo["username"],
                        color=discord.Color.from_rgb(191, 242, 255),
                    )
                    embedVar.add_field(
                        name="Long Description",
                        value=str(getOneBotInfo["longdesc"])
                        .replace("\r", "")
                        .replace("\n", ""),
                        inline=False,
                    )
                    embedVar.add_field(
                        name="Short Description",
                        value=getOneBotInfo["shortdesc"],
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Prefix", value=getOneBotInfo["prefix"], inline=True
                    )
                    embedVar.add_field(
                        name="GitHub",
                        value=str(getOneBotInfo["github"])
                        .replace('"', "")
                        .replace("'", ""),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Website",
                        value=str(getOneBotInfo["website"])
                        .replace('"', "")
                        .replace("'", ""),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Invite",
                        value=str(getOneBotInfo["invite"]),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Points",
                        value=str(getOneBotInfo["points"]),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Certified Bot",
                        value=str(getOneBotInfo["certifiedBot"]),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Owners",
                        value=str(getOneBotInfo["owners"]).replace("'", ""),
                        inline=True,
                    )
                    embedVar.add_field(
                        name="Tags",
                        value=str(getOneBotInfo["tags"]).replace("'", ""),
                        inline=True,
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
            headers = {"Authorization": key}
            async with session.get(
                f"https://top.gg/api/users/{search}", headers=headers
            ) as response:
                user = await response.json()
                try:
                    if str(user["error"]) in "Not found":
                        embedVar = discord.Embed(
                            color=discord.Color.from_rgb(255, 51, 51)
                        )
                        embedVar.description = (
                            "The user was not found. Please try again."
                        )
                        embedVar.add_field(
                            name="Reason", value=user["error"], inline=True
                        )
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar = discord.Embed(
                            title=user["username"],
                            color=discord.Color.from_rgb(191, 242, 255),
                        )
                        embedVar.add_field(
                            name="Bio", value=user["bio"], inline=True)
                        embedVar.add_field(
                            name="Admin", value=user["admin"], inline=True
                        )
                        embedVar.add_field(
                            name="Web Mod", value=user["webMod"], inline=True
                        )
                        embedVar.add_field(
                            name="Mod", value=user["mod"], inline=True)
                        embedVar.add_field(
                            name="Certified Dev",
                            value=user["certifiedDev"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Supporter", value=user["supporter"], inline=True
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
