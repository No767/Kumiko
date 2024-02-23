from __future__ import annotations

import asyncio
import importlib
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from discord.ext import commands
from watchfiles import Change, awatch

if TYPE_CHECKING:
    from bot.kumikocore import KumikoCore


class Reloader:
    """An watchdog for reloading extensions and library files

    This reloads/unloads extensions, and also reloads library modules.
    This does not implement a deep reload, as there is no way to do so
    that way.
    """

    def __init__(self, bot: KumikoCore, path: Path):
        self.bot = bot
        self.path = path

        self.loop = asyncio.get_running_loop()
        self.logger = bot.logger
        self._cogs_path = self.path / "cogs"
        self._libs_path = self.path / "libs"

    ### Finding modules from the path directly

    def find_modules_from_path(self, path: str) -> Optional[str]:
        root, ext = os.path.splitext(path)
        sys_path_index = len(sys.path[0].split("/"))
        if ext != ".py":
            return

        local_path = root.split("/")[sys_path_index:]
        return ".".join(item for item in local_path)

    ### Loading/reloading extensions and library modules

    async def reload_or_load_extension(self, module: str) -> None:
        try:
            await self.bot.reload_extension(module)
            self.logger.info("Reloaded extension: %s", module)
        except commands.ExtensionNotLoaded:
            await self.bot.load_extension(module)
            self.logger.info("Loaded extension: %s", module)

    async def reload_library(self, module: str) -> None:
        try:
            actual_module = sys.modules[module]
            importlib.reload(actual_module)
            self.logger.info("Reloaded lib module: %s", module)
        except KeyError:
            self.logger.warning("Failed to reload module %s. Does it exist?", module)

    async def reload_extension_or_library(self, module: str) -> None:
        if module.startswith("libs"):
            await self.reload_library(module)
        elif module.startswith("cogs"):
            await self.reload_or_load_extension(module)

    ### Internal coroutine to start the watch

    async def _start(self) -> None:
        async for changes in awatch(self._cogs_path, self._libs_path):
            for ctype, cpath in changes:
                module = self.find_modules_from_path(cpath)
                if module is None:
                    continue

                if ctype == Change.modified or ctype == Change.added:
                    await self.reload_extension_or_library(module)
                elif ctype == Change.deleted:
                    await self.bot.unload_extension(module)

    ### Public method to start the reloader

    def start(self) -> None:
        """Starts the deep reloader"""
        self.loop.create_task(self._start())
        self.bot.dispatch("reloader_ready")
