import logging
from pathlib import Path as SyncPath

import discord
from anyio import Path
from discord.ext import commands
from Libs.utils.help import KumikoHelp
from Libs.utils.redis import redisCheck

# Some weird import logic to ensure that watchfiles is there
_fsw = True
try:
    from watchfiles import awatch
except ImportError:
    _fsw = False


class KumikoCore(commands.Bot):
    """The core of Kumiko - Subclassed this time"""

    def __init__(
        self,
        intents: discord.Intents,
        dev_mode: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned_or(">"),
            help_command=KumikoHelp(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help"),
            *args,
            **kwargs,
        )
        self.dev_mode = dev_mode
        self.logger: logging.Logger = logging.getLogger("kumikobot")

    async def fsWatcher(self) -> None:
        cogsPath = SyncPath(__file__).parent.joinpath("Cogs")
        async for changes in awatch(cogsPath):
            changesList = list(changes)[0]
            if changesList[0].modified == 2:
                reloadFile = SyncPath(changesList[1])
                self.logger.info(f"Reloading extension: {reloadFile.name[:-3]}")
                await self.reload_extension(f"Cogs.{reloadFile.name[:-3]}")

    async def setup_hook(self) -> None:
        cogsPath = Path(__file__).parent.joinpath("Cogs")
        async for cog in cogsPath.rglob("**/*.py"):
            if cog.parent.name == "Cogs":
                self.logger.debug(
                    f"Loaded extension: {cog.parent.name}.{cog.name[:-3]}"
                )
                await self.load_extension(f"{cog.parent.name}.{cog.name[:-3]}")
            else:
                self.logger.debug(
                    f"Loaded extension: Cogs.{cog.parent.name}.{cog.name[:-3]}"
                )
                await self.load_extension(f"Cogs.{cog.parent.name}.{cog.name[:-3]}")

        self.loop.create_task(redisCheck())

        if self.dev_mode is True and _fsw is True:
            self.logger.info("Dev mode is enabled. Loading Jishaku and FSWatcher")
            self.loop.create_task(self.fsWatcher())
            await self.load_extension("jishaku")

    async def on_ready(self):
        currUser = None if self.user is None else self.user.name
        self.logger.info(f"{currUser} is fully ready!")
