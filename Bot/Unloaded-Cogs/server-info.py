import asyncio
import random

import discord
import uvloop
from discord.ext import commands


def pickColor():
    colors = [0x8B77BE, 0xA189E2, 0xCF91D1, 0x5665AA, 0xA3A3D2]
    return random.choice(colors)  # nosec B311


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo", help="Known server information")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        name = guild.name
        channels = guild.channels
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        members = guild.member_count
        premium_members = guild.premium_subscription_count
        max_members = guild.max_members
        location = guild.region
        epox = guild.created_at
        explicit = guild.explicit_content_filter
        emojis = guild.emojis
        embed = discord.Embed(color=pickColor())
        embed.title = "Server Info"
        embed.add_field(name="Name", value=name, inline=True)
        embed.add_field(name="# of channels", value=len(channels), inline=True)
        embed.add_field(
            name="# of text channels", value=len(text_channels), inline=True
        )
        embed.add_field(
            name="# of voice channels", value=len(voice_channels), inline=True
        )
        embed.add_field(
            name="# of nitro boosted members", value=premium_members, inline=True
        )
        embed.add_field(
            name="# of members", value=f"{members}/{max_members}", inline=True
        )
        embed.add_field(name="Located in", value=location, inline=True)
        embed.add_field(name="Created on", value=epox, inline=True)
        embed.add_field(
            name="Explicit content filter enabled for", value=explicit, inline=True
        )
        embed.add_field(name="List of all emojis", value=emojis, inline=True)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(Utility(bot))
