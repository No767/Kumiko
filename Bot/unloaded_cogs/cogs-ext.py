from pathlib import Path

import aiofiles
import discord
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore


class CogsExtensions(commands.Cog):
    """Utility to add custom cogs for Kumiko"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = bot.session

    @commands.hybrid_group(name="cogs-ext", alias=["cext"])
    async def cogsExt(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @cogsExt.command(name="add")
    @app_commands.describe(cog="The cog to load. Can be from GitHub")
    @commands.is_owner()
    async def cogsExtAdd(self, ctx: commands.Context, cog: discord.Attachment) -> None:
        """Adds and loads the given cog"""
        async with self.session.get(cog.url) as r:
            writeFile = Path(__file__).parent.joinpath(cog.filename)
            async with aiofiles.open(writeFile, "w") as f:
                await f.write(await r.text())
                await self.bot.load_extension(f"Cogs.{cog.filename[:-3]}")
                await ctx.send("test")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(CogsExtensions(bot))
