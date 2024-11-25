from __future__ import annotations

import asyncio
import importlib
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from discord.ext import commands
from watchfiles import Change, awatch

if TYPE_CHECKING:
    from bot.kumiko import Kumiko


class Reloader:
    def __init__(self, bot: Kumiko, root_path: Path):
        self.bot = bot
        self.loop = asyncio.get_running_loop()
        self.root_path = root_path
        self.logger = self.bot.logger
        self._cogs_path = self.root_path / "cogs"
        self._libs_path = self.root_path / "libs"

    async def reload_or_load_extension(self, module: str) -> None:
        try:
            await self.bot.reload_extension(module)
            self.logger.info("Reloaded extension: %s", module)
        except commands.ExtensionNotLoaded:
            await self.bot.load_extension(module)
            self.logger.info("Loaded extension: %s", module)

    async def reload_lib_modules(self, module: str) -> None:
        try:
            actual_module = sys.modules[module]
            importlib.reload(actual_module)
        except KeyError:
            self.logger.warning("Failed to reload module %s. Does it exist?", module)

    def find_modules_from_path(self, path: str):
        root, ext = os.path.splitext(path)
        if ext != ".py":
            return
        true_root = ".".join(root.split("/")[1:])
        return true_root

    def find_true_module(self, module: str) -> str:
        parts = module.split(".")
        if "libs" in parts:
            lib_index = parts.index("libs")
            return ".".join(parts[lib_index:])
        cog_index = parts.index("cogs")
        return ".".join(parts[cog_index:])

    async def reload_cogs_and_libs(self, ctype: Change, true_module: str) -> None:
        if true_module.startswith("cogs"):
            if ctype == Change.modified or ctype == Change.added:
                await self.reload_or_load_extension(true_module)
            elif ctype == Change.deleted:
                await self.bot.unload_extension(true_module)
        elif true_module.startswith("libs"):
            self.logger.info("Reloaded library module: %s", true_module)
            await self.reload_lib_modules(true_module)

    async def _watch_cogs(self):
        async for changes in awatch(self._cogs_path, self._libs_path, recursive=True):
            for ctype, cpath in changes:
                module = self.find_modules_from_path(cpath)
                if module is None:
                    continue

                true_module = self.find_true_module(module)
                await self.reload_cogs_and_libs(ctype, true_module)

    def start(self):
        self.loop.create_task(self._watch_cogs())
        self.bot.dispatch("reloader_ready")
