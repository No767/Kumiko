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

load_dotenv()
apiKey = os.getenv("Discord_Bots_API_Key")
parser = simdjson.Parser()


class DiscordBots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    db = SlashCommandGroup("discordbots", "Commands for Discord.bots.gg service")
    dbSearch = db.create_subgroup("search", "Search for bots on Discord.bots.gg")

    @dbSearch.command(name="bots")
    async def discordBotsSearch(
        self,
        ctx,
        *,
        search: Option(str, "The bot that you wish to search for"),
    ):
        """Searches for any Discord Bots listed on discord.bots.gg"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            params = {"q": search, "limit": 5}
            async with session.get(
                "https://discord.bots.gg/api/v1/bots", headers=headers, params=params
            ) as r:
                data = await r.content.read()
                dataMain = parser.parse(data, recursive=True)
                filterMain = [
                    "avatarURL",
                    "coOwners",
                    "shortDescription",
                    "owner",
                    "username",
                ]
                embedVar = discord.Embed()
                try:
                    if len(dataMain["bots"]) == 0:
                        raise ValueError
                    else:
                        for dictItem in dataMain["bots"]:
                            for k, v in dictItem.items():
                                if k not in filterMain:
                                    embedVar.add_field(name=k, value=v, inline=True)
                                    embedVar.remove_field(-18)
                            embedVar.title = dictItem["username"]
                            embedVar.description = dictItem["shortDescription"]
                            embedVar.set_thumbnail(url=dictItem["avatarURL"])
                            await ctx.respond(embed=embedVar)
                except ValueError:
                    embedValueError = discord.Embed()
                    embedValueError.description = "Oh no, it seems like there are no bots that matches your search. Please try again"
                    await ctx.respond(embed=embedValueError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @dbSearch.command(name="id")
    async def discordBotsID(
        self, ctx, *, bot_id: Option(str, "The ID of the Discord Bot")
    ):
        """Searches for any Discord Bots listed on discord.bots.gg via the Discord Bot's ID"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            async with session.get(
                f"https://discord.bots.gg/api/v1/bots/{bot_id}", headers=headers
            ) as response:
                data2 = await response.content.read()
                dataMain2 = parser.parse(data2, recursive=True)
                embedVar = discord.Embed()
                filterMain2 = [
                    "coOwners",
                    "avatarURL",
                    "shortDescription",
                    "owner",
                    "username",
                    "longDescription",
                ]
                try:
                    if "message" in dataMain2["message"]:
                        raise Exception
                    else:
                        for dictKey, dictVal in dataMain2.items():
                            if dictKey not in filterMain2:
                                embedVar.add_field(
                                    name=dictKey, value=dictVal, inline=True
                                )
                        for dictKey1, dictVal1 in dataMain2["owner"].items():
                            embedVar.add_field(
                                name=dictKey1, value=dictVal1, inline=True
                            )
                        embedVar.title = dataMain2["username"]
                        embedVar.description = f"{dataMain2['shortDescription']}\n\n{dataMain2['longDescription']}"
                        embedVar.set_thumbnail(url=dataMain2["avatarURL"])
                        await ctx.respond(embed=embedVar)
                except Exception:
                    embedError = discord.Embed()
                    embedError.description = (
                        "It seems like that the bot doesn't exist... Please try again"
                    )
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(DiscordBots(bot))
