from typing import Literal, Optional

import discord
from Cogs import EXTENSIONS
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context, Greedy
from kumikocore import KumikoCore

TESTING_GUILD_ID = discord.Object(id=970159505390325842)
HANGOUT_GUILD_ID = discord.Object(id=1145897416160194590)


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

    @commands.hybrid_command(name="sync", hidden=True)
    @commands.guild_only()
    @app_commands.guilds(TESTING_GUILD_ID, HANGOUT_GUILD_ID)
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

    @commands.command(name="dispatch", aliases=["dispatch-event"], hidden=True)
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_nat())
    @app_commands.guilds(TESTING_GUILD_ID)
    @app_commands.describe(event="The event to dispatch")
    async def dispatch_event(self, ctx: commands.Context, event: str) -> None:
        """Dispatches an custom event"""
        self.bot.dispatch(event, ctx.guild)
        await ctx.send("Dispatched event")

    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_nat())
    @app_commands.guilds(TESTING_GUILD_ID, HANGOUT_GUILD_ID)
    @commands.command(name="reload-all", hidden=True)
    async def upgrade(self, ctx: commands.Context) -> None:
        """Reloads all cogs. This is used for upgrading"""
        for cog in EXTENSIONS:
            await self.bot.reload_extension(cog)
        await ctx.send("Reloaded all cogs")


async def setup(bot: KumikoCore):
    await bot.add_cog(DevTools(bot))
