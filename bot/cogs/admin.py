from typing import Literal, Optional

import discord
from discord.ext import commands
from kumikocore import KumikoCore
from libs.utils.context import KContext


class Admin(commands.Cog):
    """Administrative utilities for Kumimo"""

    def __init__(self, bot: KumikoCore):
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    async def cog_check(self, ctx: KContext) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="sync", hidden="True")
    async def sync(
        self,
        ctx: KContext,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """Syncs all app commands"""
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)  # type: ignore
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Admin(bot))
