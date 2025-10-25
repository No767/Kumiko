from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, TypeVar, Union

import discord
from discord.ext import commands, menus

from utils.embeds import Embed
from utils.pages import KumikoPages

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from core import Kumiko
    from utils.context import KumikoContext

_T = TypeVar("_T")

NO_CONTROL_MSG = "This view cannot be controlled by you, sorry!"


class BlacklistPageSource(menus.AsyncIteratorPageSource):
    def __init__(self, entries: dict[str, Union[_T, Any]]):
        super().__init__(self.blacklist_iterator(entries), per_page=20)

    async def blacklist_iterator(
        self, entries: dict[str, Union[_T, Any]]
    ) -> AsyncIterator[str]:
        for key, entry in entries.items():
            yield f"{key}: {entry}"

    async def format_page(  # type: ignore
        self, menu: BlacklistPages, entries: list[str]
    ) -> discord.Embed:
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f"{index + 1}. {entry}")

        menu.embed.description = "\n".join(pages)
        return menu.embed


class BlacklistPages(KumikoPages):
    def __init__(self, entries: dict[str, Union[_T, Any]], *, ctx: KumikoContext):
        super().__init__(BlacklistPageSource(entries), ctx=ctx)
        self.embed = Embed(colour=discord.Colour.from_rgb(200, 168, 255))


class Admin(commands.Cog, command_attrs={"hidden": True}):
    """Administrative cog to handle admin tasks"""

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot

    async def cog_check(self, ctx: KumikoContext) -> bool:  # type: ignore
        return await self.bot.is_owner(ctx.author)

    @commands.guild_only()
    @commands.command(name="sync", hidden=True)
    async def sync(
        self,
        ctx: KumikoContext,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """Performs a sync of the tree. This will sync, copy globally, or clear the tree."""
        await ctx.defer()
        if not guilds:
            if spec == "~":
                synced = await self.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                self.bot.tree.copy_global_to(guild=ctx.guild)
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

    @commands.guild_only()
    @commands.group(name="blacklist", invoke_without_command=True)
    async def blacklist(self, ctx: KumikoContext) -> None:
        """Global blacklisting system - Without subcommand you are viewing the blacklist"""
        entries = self.bot.blacklist.all()
        if len(entries) == 0:
            await ctx.send("No blacklist entries found")
            return

        pages = BlacklistPages(entries, ctx=ctx)
        await pages.start()

    @blacklist.command(name="add")
    async def add(self, ctx: KumikoContext, discord_object: discord.Object) -> None:
        """Adds an ID to the global blacklist"""
        given_id = discord_object.id
        await self.bot.add_to_blacklist(given_id)
        self.bot.metrics.blacklist.users.inc()
        await ctx.send(f"Done. Added ID {given_id} to the blacklist")

    @blacklist.command(name="remove")
    async def remove(self, ctx: KumikoContext, discord_object: discord.Object) -> None:
        """Removes an ID from the global blacklist"""
        given_id = discord_object.id
        await self.bot.remove_from_blacklist(given_id)
        self.bot.metrics.blacklist.users.dec()
        await ctx.send(f"Done. Removed ID {given_id} from the blacklist")


async def setup(bot: Kumiko) -> None:
    await bot.add_cog(Admin(bot))
