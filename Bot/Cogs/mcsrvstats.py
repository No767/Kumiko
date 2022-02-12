import asyncio

import aiohttp
import discord
import orjson
import uvloop
from discord.ext import commands
from discord.commands import slash_command


class mcsrvstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="java", description="Returns info about the given Minecraft Java server", guild_ids=[866199405090308116])
    async def java(self, ctx, server: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            async with session.get(f"https://api.mcsrvstat.us/2/{server}") as r:
                mcsrv = await r.json()
                image_link = f"https://api.mcsrvstat.us/icon/{server}"
                try:
                    if str(mcsrv["online"]) == "True":
                        embedVar = discord.Embed(
                            title="Infomation (Java Edition)", color=0xC27C0E
                        )
                        embedVar.description = (
                            str(mcsrv["motd"]["clean"])
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", "")
                        )
                        excludedKeys = {"debug", "players", "motd", "icon"}

                        for k, v in mcsrv.get("players").items():
                            embedVar.add_field(
                                name=str(k).capitalize(), value=v, inline=True
                            )

                        for key, val in mcsrv.items():
                            if key not in excludedKeys:
                                embedVar.add_field(
                                    name=str(key).capitalize(), value=val, inline=True
                                )

                        for key1, value in mcsrv.get("debug").items():
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
                        for key, val in mcsrv.items():
                            if key not in excludedKeys:
                                embedVar.add_field(
                                    name=str(key).capitalize(), value=val, inline=True
                                )

                        for keyDict, valueDict in mcsrv.get("debug").items():
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
                        f"Your search for has failed. Please try again.\nReason: {e}"
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @java.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.respond(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class bedrock_mcsrvstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="bedrock", description="Returns info about the given Minecraft Bedrock server", guild_ids=[866199405090308116])
    async def bedrock(self, ctx, server: str):
        async with aiohttp.ClientSession(json_serialize=orjson.loads) as session:
            async with session.get(f"https://api.mcsrvstat.us/bedrock/2/{server}") as r:
                bedmcsrv = await r.json()
                bedimage_link = f"https://api.mcsrvstat.us/icon/{server}"
                try:
                    if str(bedmcsrv["online"]) == "True":
                        embedVar = discord.Embed(
                            title="Information (Bedrock Edition)", color=0x607D8B
                        )
                        embedVar.description = (
                            str(bedmcsrv["motd"]["clean"])
                            .replace("[", "")
                            .replace("]", "")
                            .replace("'", "")
                        )
                        excludedKeys = {"debug", "players", "motd"}
                        for keys, value in bedmcsrv.get("players").items():
                            embedVar.add_field(
                                name=str(keys).capitalize(), value=value, inline=True
                            )
                        for key, val in bedmcsrv.items():
                            if key not in excludedKeys:
                                embedVar.add_field(
                                    name=str(key).capitalize(), value=val, inline=True
                                )

                        for k, v in bedmcsrv.get("debug").items():
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
                        for key2, val2 in bedmcsrv.items():
                            if key2 not in excludedKeys2:
                                embedVar.add_field(
                                    name=str(key2).capitalize(), value=val2, inline=True
                                )

                        for key3, value3 in bedmcsrv.get("debug").items():
                            embedVar.add_field(
                                name=str(key3).capitalize(), value=value3, inline=True
                            )
                        embedVar.set_thumbnail(url=bedimage_link)
                        await ctx.respond(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed(color=0x607D8B)
                    embedVar.description = (
                        f"Your search has failed. Please try again.\nReason: {e}"
                    )
                    await ctx.respond(embed=embedVar)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @bedrock.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            msg = await ctx.respond(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(mcsrvstats(bot))
    bot.add_cog(bedrock_mcsrvstats(bot))
