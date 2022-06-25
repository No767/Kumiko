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
        """Searches for up to 1 of any Discord Bots listed on discord.bots.gg"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            params = {"q": search, "limit": 1}
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


def setup(bot):
    bot.add_cog(DiscordBots(bot))
