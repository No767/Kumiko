import asyncio
import random

import discord
import uvloop
from discord.commands import slash_command
from discord.ext import commands


def discord_colors():
    colors = [0x8B77BE, 0xA189E2, 0xCF91D1, 0x5665AA, 0xA3A3D2]
    return random.choice(colors)


def fast_embed(content):
    return discord.Embed(description=content, color=discord_colors())


class botInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="botinfo", description="Returns Stats for Rin")
    async def botinfo(self, ctx):
        bot = self.bot
        name = bot.user.name
        guilds = bot.guilds
        total_members = 0
        for guild in guilds:
            total_members += guild.member_count
        average_members_per_guild = total_members / len(guilds)
        embed = discord.Embed(color=discord_colors())
        embed.title = "Bot Info"
        embed.add_field(name="Name", value=name, inline=False)
        embed.add_field(name="Servers", value=len(guilds), inline=False)
        embed.add_field(name="Total Users", value=total_members, inline=False)
        embed.add_field(
            name="Average Users Per Server",
            value=average_members_per_guild,
            inline=False,
        )
        embed.set_thumbnail(url=bot.user.display_avatar)
        await ctx.respond(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(botInfo(bot))
