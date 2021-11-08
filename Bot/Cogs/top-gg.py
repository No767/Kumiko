import os

import discord
import requests
import ujson
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("Top_GG_API_Key")


def getBot(search):
    link = f"https://top.gg/api/bots/?search={search}"
    headers = {"Authorization": key}
    r = requests.get(link, headers=headers)
    return ujson.loads(r.text)


def getOneBot(search):
    link = f"https://top.gg/api/bots/{search}"
    headers = {"Authorization": key}
    r = requests.get(link, headers=headers)
    return ujson.loads(r.text)


def getUser(search):
    link = f"https://top.gg/api/users/{search}"
    headers = {"Authorization": key}
    r = requests.get(link, headers=headers)
    return ujson.loads(r.text)


class TopGGV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="topgg-search")
    async def topgg_search(self, ctx, *, search: str):
        try:
            getBotInfo = getBot(search)
            embedVar = discord.Embed(
                title="Top.gg Bots [Bot 1]", color=discord.Color.from_rgb(255, 232, 191)
            )
            embedVar.add_field(
                name="Username", value=getBotInfo["results"][0]["username"], inline=True
            )
            embedVar.add_field(
                name="Long Description",
                value=getBotInfo["results"][0]["longdesc"],
                inline=True,
            )
            embedVar.add_field(
                name="Short Description",
                value=getBotInfo["results"][0]["shortdesc"],
                inline=True,
            )
            embedVar.add_field(
                name="Prefix", value=getBotInfo["results"][0]["prefix"], inline=True
            )
            embedVar.add_field(
                name="GitHub",
                value=str(getBotInfo["results"][0]["github"]),
                inline=True,
            )
            embedVar.add_field(
                name="Website",
                value=str(getBotInfo["results"][0]["website"]),
                inline=True,
            )
            embedVar.add_field(
                name="Invite",
                value=str(getBotInfo["results"][0]["invite"]),
                inline=True,
            )
            embedVar.add_field(
                name="Points",
                value=str(getBotInfo["results"][0]["points"]),
                inline=True,
            )
            embedVar.add_field(
                name="Certified Bot",
                value=str(getBotInfo["results"][0]["certifiedBot"]),
                inline=True,
            )
            embedVar.add_field(
                name="Owners",
                value=str(getBotInfo["results"][0]["owners"]).replace("'", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Tags",
                value=str(getBotInfo["results"][0]["tags"]).replace("'", ""),
                inline=True,
            )
            embedVar2 = discord.Embed(
                title="Top.gg Bots [Bot 2]", color=discord.Color.from_rgb(193, 255, 191)
            )
            embedVar2.add_field(
                name="Username", value=getBotInfo["results"][0]["username"], inline=True
            )
            embedVar2.add_field(
                name="Long Description",
                value=getBotInfo["results"][0]["longdesc"],
                inline=True,
            )
            embedVar2.add_field(
                name="Short Description",
                value=getBotInfo["results"][0]["shortdesc"],
                inline=True,
            )
            embedVar2.add_field(
                name="Prefix", value=getBotInfo["results"][0]["prefix"], inline=True
            )
            embedVar2.add_field(
                name="GitHub",
                value=str(getBotInfo["results"][0]["github"]),
                inline=True,
            )
            embedVar2.add_field(
                name="Website",
                value=str(getBotInfo["results"][0]["website"]),
                inline=True,
            )
            embedVar2.add_field(
                name="Invite",
                value=str(getBotInfo["results"][0]["invite"]),
                inline=True,
            )
            embedVar2.add_field(
                name="Points",
                value=str(getBotInfo["results"][0]["points"]),
                inline=True,
            )
            embedVar2.add_field(
                name="Certified Bot",
                value=str(getBotInfo["results"][0]["certifiedBot"]),
                inline=True,
            )
            embedVar2.add_field(
                name="Owners",
                value=str(getBotInfo["results"][0]["owners"]).replace("'", ""),
                inline=True,
            )
            embedVar2.add_field(
                name="Tags",
                value=str(getBotInfo["results"][0]["tags"]).replace("'", ""),
                inline=True,
            )
            embedVar3 = discord.Embed(
                title="Top.gg Bots [Bot 3]", color=discord.Color.from_rgb(191, 242, 255)
            )
            embedVar3.add_field(
                name="Username", value=getBotInfo["results"][0]["username"], inline=True
            )
            embedVar3.add_field(
                name="Long Description",
                value=getBotInfo["results"][0]["longdesc"],
                inline=True,
            )
            embedVar3.add_field(
                name="Short Description",
                value=getBotInfo["results"][0]["shortdesc"],
                inline=True,
            )
            embedVar3.add_field(
                name="Prefix", value=getBotInfo["results"][0]["prefix"], inline=True
            )
            embedVar3.add_field(
                name="GitHub",
                value=str(getBotInfo["results"][0]["github"]),
                inline=True,
            )
            embedVar3.add_field(
                name="Website",
                value=str(getBotInfo["results"][0]["website"]),
                inline=True,
            )
            embedVar3.add_field(
                name="Invite",
                value=str(getBotInfo["results"][0]["invite"]),
                inline=True,
            )
            embedVar3.add_field(
                name="Points",
                value=str(getBotInfo["results"][0]["points"]),
                inline=True,
            )
            embedVar3.add_field(
                name="Certified Bot",
                value=str(getBotInfo["results"][0]["certifiedBot"]),
                inline=True,
            )
            embedVar3.add_field(
                name="Owners",
                value=str(getBotInfo["results"][0]["owners"]).replace("'", ""),
                inline=True,
            )
            embedVar3.add_field(
                name="Tags",
                value=str(getBotInfo["results"][0]["tags"]).replace("'", ""),
                inline=True,
            )
            await ctx.send(embed=embedVar)
            await ctx.send(embed=embedVar2)
            await ctx.send(embed=embedVar3)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(231, 74, 255))
            embedVar.description = f"The query failed. Please try again.\nReason: {e}"
            await ctx.send(embed=embedVar)

    @topgg_search.error
    async def on_message(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class TopGGV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="topgg-search-one")
    async def topgg_search_one(self, ctx, *, search: int):
        try:
            getOneBotInfo = getOneBot(search)
            embedVar = discord.Embed(
                title=getOneBotInfo["results"][0]["username"],
                color=discord.Color.from_rgb(191, 242, 255),
            )
            embedVar.add_field(
                name="Long Description",
                value=getOneBotInfo["results"][0]["longdesc"],
                inline=True,
            )
            embedVar.add_field(
                name="Short Description",
                value=getOneBotInfo["results"][0]["shortdesc"],
                inline=True,
            )
            embedVar.add_field(
                name="Prefix", value=getOneBotInfo["results"][0]["prefix"], inline=True
            )
            embedVar.add_field(
                name="GitHub",
                value=str(getOneBotInfo["results"][0]["github"]),
                inline=True,
            )
            embedVar.add_field(
                name="Website",
                value=str(getOneBotInfo["results"][0]["website"]),
                inline=True,
            )
            embedVar.add_field(
                name="Invite",
                value=str(getOneBotInfo["results"][0]["invite"]),
                inline=True,
            )
            embedVar.add_field(
                name="Points",
                value=str(getOneBotInfo["results"][0]["points"]),
                inline=True,
            )
            embedVar.add_field(
                name="Certified Bot",
                value=str(getOneBotInfo["results"][0]["certifiedBot"]),
                inline=True,
            )
            embedVar.add_field(
                name="Owners",
                value=str(getOneBotInfo["results"][0]
                          ["owners"]).replace("'", ""),
                inline=True,
            )
            embedVar.add_field(
                name="Tags",
                value=str(getOneBotInfo["results"][0]
                          ["tags"]).replace("'", ""),
                inline=True,
            )
            await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(231, 74, 255))
            embedVar.description = f"The query failed. Please try again.\nReason: {e}"
            await ctx.send(embed=embedVar)

    @topgg_search_one.error
    async def on_message(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class TopGGV3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="topgg-search-users")
    async def topgg_search_users(self, ctx, *, search: int):
        try:
            user = getUser(search)
            if str(user["error"]) in "Not found":
                embedVar = discord.Embed(
                    color=discord.Color.from_rgb(255, 51, 51))
                embedVar.description = (
                    f"The query failed. Please try again.\nReason: {user['error']}"
                )
                await ctx.send(embed=embedVar)
            else:
                embedVar = discord.Embed(
                    title=user["username"], color=discord.Color.from_rgb(
                        191, 242, 255)
                )
                embedVar.add_field(name="Bio", value=user["bio"], inline=True)
                embedVar.add_field(
                    name="Admin", value=user["admin"], inline=True)
                embedVar.add_field(
                    name="Web Mod", value=user["webMod"], inline=True)
                embedVar.add_field(name="Mod", value=user["mod"], inline=True)
                embedVar.add_field(
                    name="Certified Dev", value=user["certifiedDev"], inline=True
                )
                embedVar.add_field(
                    name="Supporter", value=user["supporter"], inline=True
                )
                await ctx.send(embed=embedVar)
        except Exception as e:
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(231, 74, 255))
            embedVar.description = f"The query failed. Please try again.\nReason: {e}"
            await ctx.send(embed=embedVar)

    @topgg_search_users.error
    async def on_message(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


def setup(bot):
    bot.add_cog(TopGGV1(bot))
    bot.add_cog(TopGGV2(bot))
    bot.add_cog(TopGGV3(bot))
