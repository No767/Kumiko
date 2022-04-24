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

apiKey = os.getenv("Blue_Alliance_API_Key")


class BlueAllianceV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="blue-alliance-team-info",
        description="Provides info about an FRC team",
        guild_ids=[866199405090308116],
    )
    async def blueAllianceTeamInfo(
        self, ctx, *, team_number: Option(int, "The FRC team number")
    ):
        async with aiohttp.ClientSession(json_serialize=orjson.dumps) as session:
            headers = {"X-TBA-Auth-Key": apiKey}
            async with session.get(
                f"https://www.thebluealliance.com/api/v3/team/frc{team_number}",
                headers=headers,
            ) as r:
                data = await r.content.read()
                dataMain = orjson.loads(data)
                embed = discord.Embed()
                embedError = discord.Embed()
                mainFilter = ["nickname", "team_number"]
                try:
                    for key, value in dataMain.items():
                        if key not in mainFilter:
                            embed.add_field(name=key, value=value, inline=True)
                    embed.title = f"{dataMain['team_number']} - {dataMain['nickname']}"
                    await ctx.respond(embed=embed)
                except Exception as e:
                    embedError.description = (
                        "Oops, something went wrong. Please try again..."
                    )
                    embedError.add_field(name="Reason", value=e, inline=True)
                    await ctx.respond(embed=embedError)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(BlueAllianceV1(bot))
