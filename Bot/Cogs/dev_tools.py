from typing import Literal, Optional

import discord
from Cogs import EXTENSIONS
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context, Greedy
from kumikocore import KumikoCore


def is_nat():
    def pred(ctx):
        return (
            ctx.guild is not None and ctx.author.id == 1028431063321686036
        )  # natalie's account

    return commands.check(pred)


class DevTools(commands.Cog, command_attrs=dict(hidden=True)):
    """Tools for developing Kumiko"""

    def __init__(self, bot: KumikoCore):
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    @commands.hybrid_command(name="sync")
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_nat())
    async def sync(
        self,
        ctx: Context,
        guilds: Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """Performs a sync of the tree. This will sync, copy globally, or clear the tree.

        Args:
            ctx (Context): Context of the command
            guilds (Greedy[discord.Object]): Which guilds to sync to. Greedily accepts a number of guilds
            spec (Optional[Literal["~", "*", "^"], optional): Specs to sync.
        """
        await ctx.defer()
        if not guilds:
            if spec == "~":
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                self.bot.tree.copy_global_to(guild=ctx.guild)  # type: ignore
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                self.bot.tree.clear_commands(guild=ctx.guild)
                await self.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await self.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await self.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.hybrid_command(name="dispatch")
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_nat())
    @app_commands.describe(event="The event to dispatch")
    async def dispatch_event(self, ctx: commands.Context, event: str) -> None:
        """Dispatches an custom event

        Args:
            ctx (commands.Context): _description_
        """
        self.bot.dispatch(event, ctx.guild)
        await ctx.send("Dispatched event")

    @commands.check_any(commands.is_owner(), is_nat())
    @commands.hybrid_command(name="arg-check", usage="<user: discord.Member>")
    async def arg_check(self, ctx: commands.Context, user: discord.Member):
        """Testing arg checks

        Args:
            user (discord.Member): The member to ping lol
        """
        raise RuntimeError("Testing moments")
        # await ctx.send(user.name)

    @commands.command(name="reload-all")
    async def upgrade(self, ctx: commands.Context) -> None:
        """Reloads all cogs. This is used for upgrading"""
        for cog in EXTENSIONS:
            await self.bot.reload_extension(cog)
        await ctx.send("Reloaded all cogs")


async def setup(bot: KumikoCore):
    await bot.add_cog(DevTools(bot))
