from __future__ import annotations

import asyncio
import importlib
import re
import subprocess  # nosec # We already know this is dangerous, but it's needed
import sys
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    NamedTuple,
    Optional,
    TypeVar,
    Union,
)

import discord
from discord.ext import commands, menus

from utils.pages.paginator import KumikoPages
from utils.view import ConfirmationView

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from core import Kumiko


GIT_PULL_REGEX = re.compile(r"^(?P<raw_filename>(?>[^|\n]+))\|\s+\d", re.MULTILINE)

NO_CONTROL_MSG = "This view cannot be controlled by you, sorry!"

_T = TypeVar("_T")


class ReloadModule(NamedTuple):
    status: bool
    module: str


class BlacklistPageSource(menus.AsyncIteratorPageSource):
    def __init__(self, entries: dict[str, Union[_T, Any]]) -> None:
        super().__init__(self.blacklist_iterator(entries), per_page=20)

    async def blacklist_iterator(
        self, entries: dict[str, Union[_T, Any]]
    ) -> AsyncIterator[str]:
        for key, entry in entries.items():
            yield f"{key}: {entry}"

    async def format_page(  # type: ignore
        self, menu: KumikoPages, entries: list[str]
    ) -> discord.Embed:
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f"{index + 1}. {entry}")

        menu.embed.description = "\n".join(pages)
        return menu.embed


class BlacklistPages(KumikoPages):
    def __init__(
        self, entries: dict[str, Union[_T, Any]], *, ctx: commands.Context
    ) -> None:
        super().__init__(BlacklistPageSource(entries), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(200, 168, 255))


class Admin(commands.Cog, command_attrs={"hidden": True}):
    """Administrative cog to handle admin tasks"""

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:  # type: ignore
        return await self.bot.is_owner(ctx.author)

    async def reload_or_load_extension(self, module: str) -> None:
        try:
            await self.bot.reload_extension(module)
        except commands.ExtensionNotLoaded:
            await self.bot.load_extension(module)

    def find_modules_from_git(self, output: str) -> list[tuple[int, str]]:
        changed_files = [
            match.group("raw_filename").strip()
            for match in GIT_PULL_REGEX.finditer(output)
        ]

        ret: list[tuple[int, str]] = []
        for file in changed_files:
            module_path = Path(file)
            root = str(module_path.parent / module_path.stem)
            ext = module_path.suffix

            if ext != ".py" or root.endswith("__init__"):
                continue

            true_root = ".".join(root.split("/")[1:])

            if true_root.startswith(("cogs", "utils")):
                # A subdirectory within these are a part of the codebase

                ret.append((true_root.count(".") + 1, true_root))

        # For reload order, the submodules should be reloaded first
        ret.sort(reverse=True)
        return ret

    async def run_process(self, command: str) -> list[str]:
        process = await asyncio.create_subprocess_shell(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        result = await process.communicate()

        return [output.decode() for output in result]

    def tick(self, label: Optional[str] = None, *, opt: Optional[bool]) -> str:
        lookup = {
            True: "\U00002705",
            False: "\U0000274c",
            None: "\U000023e9",
        }
        emoji = lookup.get(opt, "\U0000274c")
        if label is not None:
            return f"{emoji}: {label}"
        return emoji

    def format_results(self, statuses: list[ReloadModule]) -> str:
        desc = "\U00002705 - Successful reload | \U0000274c - Failed reload | \U000023e9 - Skipped\n\n"
        status = "\n".join(
            f"- {self.tick(opt=status)}: `{module}`" for status, module in statuses
        )
        desc += status
        return desc

    async def reload_ext(self, module: str) -> ReloadModule:
        try:
            await self.reload_or_load_extension(module)
            return ReloadModule(True, module)
        except commands.ExtensionError:
            return ReloadModule(False, module)

    def reload_lib_module(self, module: str) -> ReloadModule:
        try:
            actual_module = sys.modules[module]
            importlib.reload(actual_module)
            return ReloadModule(True, module)
        except KeyError:
            return ReloadModule(None, module)
        except (ImportError, SyntaxError):
            return ReloadModule(False, module)

    async def prompt(
        self,
        ctx: commands.Context,
        message: str,
        *,
        view_timeout: float = 60.0,
        delete_after: bool = True,
    ) -> Optional[bool]:
        view = ConfirmationView(ctx, timeout=view_timeout, delete_after=delete_after)
        view.message = await ctx.send(message, view=view, ephemeral=delete_after)
        await view.wait()
        return view.value

    @commands.guild_only()
    @commands.command(name="sync", hidden=True)
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^", "&"]] = None,
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
            elif spec == "&":
                self.bot.tree.clear_commands()
                synced = await self.bot.tree.sync()
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

    @commands.command(name="reload-all", hidden=True)
    async def reload(self, ctx: commands.Context) -> None:
        """Reloads all cogs and utils"""
        async with ctx.typing():
            stdout, _ = await self.run_process("git pull")

        # progress and stuff is redirected to stderr in git pull
        # however, things like "fast forward" and files
        # along with the text "already up-to-date" are in stdout

        if stdout.startswith("Already up-to-date."):
            await ctx.send(stdout)
            return

        modules = self.find_modules_from_git(stdout)

        mods_text = "\n".join(
            f"{index}. `{module}`" for index, (_, module) in enumerate(modules, start=1)
        )
        prompt_text = (
            f"This will update the following modules, are you sure?\n{mods_text}"
        )

        confirm = await self.prompt(ctx, prompt_text)
        if not confirm:
            await ctx.send("Aborting....")
            return

        statuses: list[ReloadModule] = []
        for is_submodule, module in modules:
            if is_submodule:
                statuses.extend(self.reload_lib_module(module))
            else:
                ext = await self.reload_ext(module)
                statuses.extend(ext)

        if not statuses:
            await ctx.send("No modules were reloaded")
            return

        await ctx.send(self.format_results(statuses))

    @commands.guild_only()
    @commands.group(name="blacklist", invoke_without_command=True)
    async def blacklist(self, ctx: commands.Context) -> None:
        """Global blacklisting system - Without subcommand you are viewing the blacklist"""
        entries = self.bot.blacklist.all()
        if len(entries) == 0:
            await ctx.send("No blacklist entries found")
            return

        pages = BlacklistPages(entries, ctx=ctx)
        await pages.start()

    @blacklist.command(name="add")
    async def add(self, ctx: commands.Context, obj: discord.Object) -> None:
        """Adds an ID to the global blacklist"""
        await self.bot.add_to_blacklist(obj.id)
        self.bot.metrics.blacklist.users.inc()
        await ctx.send(f"Done. Added ID {obj.id} to the blacklist")

    @blacklist.command(name="remove")
    async def remove(self, ctx: commands.Context, obj: discord.Object) -> None:
        """Removes an ID from the global blacklist"""
        await self.bot.remove_from_blacklist(obj.id)
        self.bot.metrics.blacklist.users.dec()
        await ctx.send(f"Done. Removed ID {obj.id} from the blacklist")


async def setup(bot: Kumiko) -> None:
    await bot.add_cog(Admin(bot))
