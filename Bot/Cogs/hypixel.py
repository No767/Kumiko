import os

import aiohttp
import discord
import orjson
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

hypixel_api_key = os.getenv("Hypixel_API_Key")


class hypixel_api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hypixel")
    async def hypixel(self, ctx, *, uuid: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"uuid": uuid, "key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/player", params=params
            ) as r:
                player = await r.json()
                async with aiohttp.ClientSession(
                    json_serialize=orjson.dumps
                ) as session1:
                    params = {"uuid": uuid, "key": hypixel_api_key}
                    async with session1.get(
                        "https://api.hypixel.net/status", params=params
                    ) as r1:
                        online = await r1.json()
                        http_statusv1 = r.status
                        try:
                            if str(player["success"]) == "True":
                                discord_embed = discord.Embed(
                                    title="Player Info",
                                    color=discord.Color.from_rgb(
                                        186, 244, 255),
                                )
                                discord_embed.add_field(
                                    name="Username",
                                    value=player["player"]["displayname"],
                                    inline=True,
                                )
                                discord_embed.add_field(
                                    name="ID",
                                    value=player["player"]["_id"],
                                    inline=True,
                                )
                                discord_embed.add_field(
                                    name="UUID",
                                    value=player["player"]["uuid"],
                                    inline=True,
                                )
                                discord_embed.add_field(
                                    name="Known Aliases",
                                    value=str(player["player"]["knownAliases"])
                                    .replace("'", "")
                                    .replace("[", "")
                                    .replace("]", ""),
                                    inline=True,
                                )
                                discord_embed.add_field(
                                    name="Online Status",
                                    value=online["session"]["online"],
                                    inline=True,
                                )
                                discord_embed.add_field(
                                    name="Success or Not?",
                                    value=player["success"],
                                    inline=True,
                                )
                                discord_embed.add_field(
                                    name="HTTP Status (Hypixel API)",
                                    value=str(http_statusv1),
                                    inline=True,
                                )
                                await ctx.send(embed=discord_embed)
                            else:
                                embedVar = discord.Embed()
                                embedVar.description = f"The query was not successful.\nDebug:\nSuccess (Player) >> {player['success']}\nCause (Player) >> {player['cause']}\nHTTP Status (Hypixel API) >> {http_statusv1}"
                                await ctx.send(embed=embedVar)
                        except Exception as e:
                            embedVar = discord.Embed()
                            embedVar.description = "The query was not successful."
                            embedVar.add_field(
                                name="Reason", value=e, inline=True)
                            await ctx.send(embed=embedVar)

    @hypixel.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class hypixel_player_count(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hypixelcount")
    async def player_count(self, ctx):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/counts", params=params
            ) as response:
                status = await response.json()
                http_status = response.status
                try:
                    if str(status["success"]) == "True":
                        embedVar = discord.Embed(
                            title="Games Player Count",
                            color=discord.Color.from_rgb(186, 193, 255),
                        )
                        embedVar.add_field(
                            name="Main Lobby",
                            value=status["games"]["MAIN_LOBBY"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Tournament Lobby",
                            value=status["games"]["TOURNAMENT_LOBBY"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="SMP",
                            value=status["games"]["SMP"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Housing",
                            value=status["games"]["HOUSING"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Pit",
                            value=status["games"]["PIT"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="TNTGames",
                            value=status["games"]["TNTGAMES"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Replay",
                            value=status["games"]["REPLAY"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Bedwars",
                            value=status["games"]["BEDWARS"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Survival Games",
                            value=status["games"]["SURVIVAL_GAMES"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Skyblock",
                            value=status["games"]["SKYBLOCK"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="UHC",
                            value=status["games"]["UHC"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Arcade",
                            value=status["games"]["ARCADE"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Build Battle",
                            value=status["games"]["BUILD_BATTLE"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Duels",
                            value=status["games"]["DUELS"]["players"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="HTTP Status (Hypixel API)",
                            value=str(http_status),
                            inline=False,
                        )
                        await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The command broke. Please try again."
                    embedVar.add_field(
                        name="Reason", value=str(e), inline=False)
                    await ctx.send(embed=embedVar)


class hypixel_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hypixelplayerstatus")
    async def player_status(self, ctx, *, uuid: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"uuid": uuid, "key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/status", params=params
            ) as rep:
                player_statusv3 = await rep.json()
                http_statusv1 = rep.status
                try:
                    if str(player_statusv3["success"]) == "True":
                        embedVar = discord.Embed(
                            title="Player Status",
                            color=discord.Color.from_rgb(222, 222, 222),
                        )
                        embedVar.add_field(
                            name="UUID", value=player_statusv3["uuid"], inline=True
                        )
                        embedVar.add_field(
                            name="Online",
                            value=player_statusv3["session"]["online"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Success",
                            value=player_statusv3["success"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="HTTP Status", value=http_statusv1, inline=True
                        )
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar = discord.Embed()
                        embedVar.description = f"The query was not successful.\nDebug:\nSuccess >> {player_statusv3['success']}\nCause >> {player_statusv3['cause']}\nHTTP Status (Hypixel API)>> {http_statusv1}"
                        await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = "The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    @player_status.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


class skywars(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skywarsinfo")
    async def skywars_info(self, ctx, *, uuid: str):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            params = {"uuid": uuid, "key": hypixel_api_key}
            async with session.get(
                "https://api.hypixel.net/player/ranked/skywars", params=params
            ) as re:
                skywars = await re.json()
                http_statusv1 = re.status
                try:
                    if str(skywars["success"]) == "True":
                        embedVar = discord.Embed(
                            title="Skywars Position",
                            color=discord.Color.from_rgb(255, 143, 143),
                        )
                        embedVar.add_field(
                            name="Position",
                            value=skywars["results"]["position"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="Score", value=skywars["results"]["score"], inline=True
                        )
                        embedVar.add_field(
                            name="Success or Not?",
                            value=skywars["success"],
                            inline=True,
                        )
                        embedVar.add_field(
                            name="HTTP Status (Hypixel API)",
                            value=http_statusv1,
                            inline=True,
                        )
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar = discord.Embed()
                        embedVar.description = "The given player either does not exist or has not played Ranked Skywars yet."
                        embedVar.add_field(
                            name="Success", value=skywars["success"], inline=True
                        )
                        embedVar.add_field(
                            name="Cause", value=skywars["cause"], inline=True
                        )
                        embedVar.add_field(
                            name="HTTP Status", value=http_statusv1, inline=True
                        )
                        await ctx.send(embed=embedVar)
                except Exception as e:
                    embedVar = discord.Embed()
                    embedVar.description = f"The query was not successful."
                    embedVar.add_field(name="Reason", value=e, inline=True)
                    await ctx.send(embed=embedVar)

    @skywars_info.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a requireed argument: {error.param}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


def setup(bot):
    bot.add_cog(hypixel_api(bot))
    bot.add_cog(hypixel_status(bot))
    bot.add_cog(hypixel_player_count(bot))
    bot.add_cog(skywars(bot))
