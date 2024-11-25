from typing import Literal, Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context, Greedy
from libs.utils import WebhookDispatcher
from libs.utils.context import KumikoContext

from bot.kumiko import Kumiko
from cogs import EXTENSIONS

TESTING_GUILD_ID = discord.Object(id=970159505390325842)
HANGOUT_GUILD_ID = discord.Object(id=1145897416160194590)


class DevTools(commands.Cog, command_attrs=dict(hidden=True)):
    """Tools for developing Kumiko"""

    def __init__(self, bot: Kumiko):
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    async def cog_check(self, ctx: KumikoContext) -> bool:
        return await self.bot.is_owner(ctx.author) and ctx.guild is not None

    @commands.command(name="sync", hidden=True)
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
    async def dispatch_event(self, ctx: KumikoContext, event: str) -> None:
        """Dispatches an custom event"""
        self.bot.dispatch(event, ctx.guild)
        await ctx.send("Dispatched event")

    @commands.command(name="reload-all", hidden=True)
    async def upgrade(self, ctx: KumikoContext) -> None:
        """Reloads all cogs. This is used for upgrading"""
        for cog in EXTENSIONS:
            await self.bot.reload_extension(cog)
        await ctx.send("Reloaded all cogs")

    @commands.command(name="raise-error", hidden=True)
    async def raise_error(self, ctx: KumikoContext) -> None:
        """Simple test command"""
        raise RuntimeError("Invalid...")

    @commands.command(name="dispatch-logs-webhook")
    async def dispatch_webhook(self, ctx: KumikoContext, *, content: str) -> None:
        """Dispatch the webhook logs event"""
        assert ctx.guild is not None
        dispatcher = WebhookDispatcher(self.bot, ctx.guild.id)
        wb = await dispatcher.get_webhook()
        if wb is None:
            await ctx.send("Guild does no have logs webhook. Aborting")
            return
        await wb.send(content=content)
        await ctx.send(f"Webhook dispatched with message: {content}")


async def setup(bot: Kumiko):
    await bot.add_cog(DevTools(bot))
