import asyncio

import aiohttp
import discord
import orjson
import simdjson
import uvloop
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands

parser = simdjson.Parser()


class MCSrvStatsV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    mc = SlashCommandGroup("minecraft", "Commands for Minecraft Server Stats")

    @mc.command(name="java")
    async def javaCheck(
        self, ctx, server: Option(str, "The Minecraft server IP or hostname")
    ):
        """Checks and returns info about the given Minecraft Java server"""
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.mcsrvstat.us/2/{server}") as r:
                mcsrv = await r.content.read()
                mcsrvMain = parser.parse(mcsrv, recursive=True)
                image_link = f"https://api.mcsrvstat.us/icon/{server}"
                try:
                    if str(mcsrvMain["online"]) == "True":
                        embedVar = discord.Embed(
                            title="Infomation (Java Edition)", color=0xC27C0E
                        )
                        embedVar.description = (
                            str(mcsrvMain["motd"]["clean"])
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", "")
                        )
                        excludedKeys = {"debug", "players", "motd", "icon"}

                        for k, v in mcsrvMain.get("players").items():
                            embedVar.add_field(
                                name=str(k).capitalize(), value=v, inline=True
                            )

                        for key, val in mcsrvMain.items():
                            if key not in excludedKeys:
                                embedVar.add_field(
                                    name=str(key).capitalize(), value=val, inline=True
                                )

                        for key1, value in mcsrvMain.get("debug").items():
                            embedVar.add_field(
                                name=str(key1).capitalize(), value=value, inline=True
                            )

                        embedVar.add_field(
                            name="HTTP Status (McSrvStat)", value=r.status, inline=True
                        )
                        embedVar.set_thumbnail(url=image_link)
                        await ctx.respond(embed=embedVar)
                    else:
                        embedVar = discord.Embed(
                            title="Infomation (Java Edition)", color=0xC27C0E
                        )
                        excludedKeys = {"debug"}
                        for key, val in mcsrvMain.items():
                            if key not in excludedKeys:
                                embedVar.add_field(
                                    name=str(key).capitalize(), value=val, inline=True
                                )

                        for keyDict, valueDict in mcsrvMain.get("debug").items():
                            embedVar.add_field(
                                name=str(keyDict).capitalize(),
                                value=valueDict,
                                inline=True,
                            )

                        embedVar.add_field(
                            name="HTTP Status (MCSrvStat)",
                            value=r.status,
                            inline=True,
                        )
                        embedVar.set_thumbnail(url=image_link)
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(color=0xC27C0E)
                    embedVar.description = (
                        f"Your search for has failed. Please try again."
                    )
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @mc.command(name="bedrock")
    async def bedrockCheck(
        self, ctx, server: Option(str, "The Minecraft server IP or hostname")
    ):
        """Returns the status and info of any Bedrock or Geyser-compatible server"""
        async with aiohttp.ClientSession(json_serialize=orjson.loads) as session:
            async with session.get(f"https://api.mcsrvstat.us/bedrock/2/{server}") as r:
                bedmcsrv = await r.content.read()
                bedmcsrvMain = parser.parse(bedmcsrv, recursive=True)
                bedimage_link = f"https://api.mcsrvstat.us/icon/{server}"
                try:
                    if str(bedmcsrvMain["online"]) == "True":
                        embedVar = discord.Embed(
                            title="Information (Bedrock Edition)", color=0x607D8B
                        )
                        embedVar.description = (
                            str(bedmcsrvMain["motd"]["clean"])
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", "")
                        )
                        excludedKeys = {"debug", "players", "motd"}
                        for keys, value in bedmcsrvMain.get("players").items():
                            embedVar.add_field(
                                name=str(keys).capitalize(), value=value, inline=True
                            )
                        for key, val in bedmcsrvMain.items():
                            if key not in excludedKeys:
                                embedVar.add_field(
                                    name=str(key).capitalize(), value=val, inline=True
                                )

                        for k, v in bedmcsrvMain.get("debug").items():
                            embedVar.add_field(
                                name=str(k).capitalize(), value=v, inline=True
                            )

                        embedVar.add_field(
                            name="HTTP Status (McSrvStat)", value=r.status, inline=True
                        )
                        embedVar.set_thumbnail(url=bedimage_link)
                        await ctx.respond(embed=embedVar)
                    else:
                        embedVar = discord.Embed(
                            title="Information (Bedrock Edition)", color=0x607D8B
                        )
                        excludedKeys2 = {"debug"}
                        for key2, val2 in bedmcsrvMain.items():
                            if key2 not in excludedKeys2:
                                embedVar.add_field(
                                    name=str(key2).capitalize(), value=val2, inline=True
                                )

                        for key3, value3 in bedmcsrvMain.get("debug").items():
                            embedVar.add_field(
                                name=str(key3).capitalize(), value=value3, inline=True
                            )
                        embedVar.set_thumbnail(url=bedimage_link)
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(color=0x607D8B)
                    embedVar.description = f"Your search has failed. Please try again."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(MCSrvStatsV1(bot))
