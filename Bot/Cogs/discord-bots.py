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
apiKey = os.getenv("Discord_Bots_API_Key")
jsonParser = simdjson.Parser()


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
        """Searches for up to 25 of any Discord Bots listed on discord.bots.gg"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"Authorization": apiKey}
            params = {"q": search, "limit": 25}
            async with session.get(
                "https://discord.bots.gg/api/v1/bots", headers=headers, params=params
            ) as r:
                data = await r.content.read()
                dataMain = jsonParser.parse(data, recursive=True)
                try:
                    if len(dataMain["bots"]) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=mainItem["username"],
                                    description=mainItem["shortDescription"],
                                )
                                .add_field(
                                    name="Bot ID", value=mainItem["userId"], inline=True
                                )
                                .add_field(
                                    name="Prefix", value=mainItem["prefix"], inline=True
                                )
                                .add_field(
                                    name="Help Command",
                                    value=mainItem["helpCommand"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Discord Libary Name",
                                    value=mainItem["libraryName"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Website",
                                    value=mainItem["website"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Support Invite",
                                    value=mainItem["supportInvite"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Guild Count",
                                    value=mainItem["guildCount"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Online", value=mainItem["online"], inline=True
                                )
                                .add_field(
                                    name="Added Date",
                                    value=parser.isoparse(
                                        mainItem["addedDate"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Owner",
                                    value=mainItem["owner"]["username"],
                                    inline=True,
                                )
                                .set_thumbnail(url=mainItem["avatarURL"])
                                for mainItem in dataMain["bots"]
                            ],
                            loop_pages=True,
                        )
                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedValueError = discord.Embed()
                    embedValueError.description = "Oh no, it seems like there are no bots that matches your search. Please try again"
                    await ctx.respond(embed=embedValueError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(DiscordBots(bot))
