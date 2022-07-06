import platform

import discord
from discord.commands import slash_command
from discord.ext import commands


class PlatformV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="kumiko-platform",
        description="Provides info about the current platform being used",
    )
    async def platformChecker(self, ctx):
        embed = discord.Embed()
        embed.add_field(name="System", value=platform.system(), inline=True)
        embed.add_field(name="System Version", value=platform.version(), inline=True)
        embed.add_field(
            name="Processor", value=f"[{platform.processor()}]", inline=True
        )
        embed.add_field(name="Machine", value=platform.machine(), inline=True)
        embed.add_field(
            name="Python Compiler", value=platform.python_compiler(), inline=True
        )
        embed.add_field(
            name="Python Version", value=platform.python_version(), inline=True
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(PlatformV1(bot))
