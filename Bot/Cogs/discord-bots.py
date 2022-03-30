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
apiKey = os.getenv("Discord_Bots_API_Key")


class DiscordBotsV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="discord-bots-search",
        description="Searches for any Discord Bots listed on discord.bots.gg",
    )
    async def discordBotsSearch(
        self,
        ctx,
        *,
        search: Option(str, "The bot that you wish to search for"),
        sort: Option(
            str,
            "Sorts the results via the given keys",
            choices=["username", "id", "guildcount", "library", "author"],
        ),
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            params = {"q": search, "sort": sort, "limit": 5}
            async with session.get(
                "https://discord.bots.gg/api/v1/bots", headers=headers, params=params
            ) as r:
                data = await r.content.read()
                dataMain = orjson.loads(data)
                filterMain = [
                    "avatarURL",
                    "coOwners",
                    "shortDescription",
                    "owner",
                    "username",
                ]
                embedVar = discord.Embed()
                try:
                    for dictItem in dataMain["bots"]:
                        for k, v in dictItem.items():
                            if k not in filterMain:
                                embedVar.add_field(
                                    name=k, value=v, inline=True)
                        for keys, value in dictItem["owner"].items():
                            embedVar.add_field(
                                name=keys, value=value, inline=True)
                        embedVar.title = dictItem["username"]
                        embedVar.description = dictItem["shortDescription"]
                        embedVar.set_thumbnail(url=dictItem["avatarURL"])
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    print(dataMain)
                    embedError = discord.Embed()
                    embedError.description = (
                        "It seems like it didn't work... Please try again"
                    )
                    embedError.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DiscordBotsV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="discord-bots-id",
        description="Searches for any Discord Bots listed on discord.bots.gg via the Discord Bot's ID",
    )
    async def discordBotsID(
        self, ctx, *, bot_id: Option(str, "The ID of the Discord Bot")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            async with session.get(
                f"https://discord.bots.gg/api/v1/bots/{bot_id}", headers=headers
            ) as response:
                data2 = await response.content.read()
                dataMain2 = orjson.loads(data2)
                embedVar = discord.Embed()
                filterMain2 = [
                    "coOwners",
                    "avatarURL",
                    "shortDescription",
                    "owner",
                    "username",
                    "longDescription",
                ]
                for dictKey, dictVal in dataMain2.items():
                    if dictKey not in filterMain2:
                        embedVar.add_field(
                            name=dictKey, value=dictVal, inline=True)
                for dictKey1, dictVal1 in dataMain2["owner"].items():
                    embedVar.add_field(
                        name=dictKey1, value=dictVal1, inline=True)
                embedVar.title = dataMain2["username"]
                embedVar.description = (
                    f"{dataMain2['shortDescription']}\n\n{dataMain2['longDescription']}"
                )
                embedVar.set_thumbnail(url=dataMain2["avatarURL"])
                await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(DiscordBotsV1(bot))
    bot.add_cog(DiscordBotsV2(bot))
