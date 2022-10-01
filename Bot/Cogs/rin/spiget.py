import asyncio
from datetime import datetime

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from rin_exceptions import NoItemsError

parser = simdjson.Parser()


class SpigetV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    spiget = SlashCommandGroup("spigot", "Commands for Spiget")

    @spiget.command(name="search")
    async def spigetSearch(self, ctx, *, name: Option(str, "The name of the plugin")):
        """Finds up to 25 plugins matching the name of the given plugin"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"
            }
            params = {"size": 25}
            async with session.get(
                f"https://api.spiget.org/v2/search/resources/{str(name).lower()}",
                headers=headers,
                params=params,
            ) as r:
                resource = await r.content.read()
                resourceMain = parser.parse(resource, recursive=True)
                try:
                    if len(resourceMain) == 0:
                        raise NoItemsError
                    else:
                        mainPages = pages.Paginator(
                            pages=[
                                discord.Embed(
                                    title=mainItem["name"], description=mainItem["tag"]
                                )
                                .add_field(
                                    name="Tested MC Versions",
                                    value=str(mainItem["testedVersions"]).replace(
                                        "'", ""
                                    ),
                                    inline=True,
                                )
                                .add_field(
                                    name="Average Rating",
                                    value=round(mainItem["rating"]["average"]),
                                    inline=True,
                                )
                                .add_field(
                                    name="Downloads",
                                    value=mainItem["downloads"],
                                    inline=True,
                                )
                                .add_field(
                                    name="Release Date",
                                    value=datetime.fromtimestamp(
                                        mainItem["releaseDate"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Last Updated",
                                    value=datetime.fromtimestamp(
                                        mainItem["updateDate"]
                                    ).strftime("%Y-%m-%d %H:%M:%S"),
                                    inline=True,
                                )
                                .add_field(
                                    name="Download Link",
                                    value=f'https://spigotmc.org/{mainItem["file"]["url"]}',
                                    inline=True,
                                )
                                .set_thumbnail(
                                    url=f'https://www.spigotmc.org/{mainItem["icon"]["url"]}'
                                )
                                for mainItem in resourceMain
                            ],
                            loop_pages=True,
                        )

                        await mainPages.respond(ctx.interaction, ephemeral=False)
                except NoItemsError:
                    embedErrorMain = discord.Embed()
                    embedErrorMain.description = "No results found... Please try again"
                    await ctx.respond(embed=embedErrorMain)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(SpigetV1(bot))
