import logging
from pathlib import Path as SyncPath

import asyncpg
import discord
from aiohttp import ClientSession
from anyio import Path
from discord.ext import commands
from Libs.utils import get_prefix
from Libs.utils.help import KumikoHelpPaginated
from Libs.utils.postgresql import ensureOpenPostgresConn
from Libs.utils.redis import ensureOpenRedisConn
from lru import LRU

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
        session: ClientSession,
        pool: asyncpg.Pool,
        lru_size: int = 50,
        dev_mode: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(
            intents=intents,
            command_prefix=get_prefix,
            help_command=KumikoHelpPaginated(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help"),
            *args,
            **kwargs,
        )
        self.dev_mode = dev_mode
        self.lru_size = lru_size
        self._session = session
        self._pool = pool
        self._prefixes: LRU = LRU(self.lru_size)
        self.default_prefix = ">"
        self.logger: logging.Logger = logging.getLogger("kumikobot")

    @property
    def session(self) -> ClientSession:
        """A global web session used throughout the lifetime of the bot

        Returns:
            ClientSession: AIOHTTP's ClientSession
        """
        return self._session

    @property
    def pool(self) -> asyncpg.Pool:
        """A global object managed throughout the lifetime of Kumiko

        Holds the asyncpg

        Returns:
            asyncpg.Pool: asyncpg connection pool
        """
        return self._pool

    # It is preffered in this case to keep an LRU cache instead of a regular Dict cache
    # For example, if an running instance keeps 100 entries ({guild_id: prefix})
    # then this would take up too much memory.
    #
    # By instead using an LRU cache, if we reach the max, then we evict the prefix from the guild that hasn't used it in a while
    # The limit for the LRU cache is set to 100
    #
    # The primary goal of Kumiko is to keep the footprint of the RAM usage as low as possible
    # We don't need to have the bot consuming 250-300MB of RAM like when Prisma was used.
    @property
    def prefixes(self) -> LRU:
        """A LRU cache of the guild prefixes

        The LRU cache's implementation is built in C,
        so we natively can keep the performance the same as if it was a regular dict

        Returns:
            LRU: LRU cache of the guild prefixes
        """
        return self._prefixes

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
            self.logger.debug(f"Loaded extension: {cog.parent.name}.{cog.name[:-3]}")
            await self.load_extension(f"{cog.parent.name}.{cog.name[:-3]}")

        self.loop.create_task(ensureOpenPostgresConn(self._pool))
        self.loop.create_task(ensureOpenRedisConn())

        if self.dev_mode is True and _fsw is True:
            self.logger.info("Dev mode is enabled. Loading Jishaku and FSWatcher")
            self.loop.create_task(self.fsWatcher())
            await self.load_extension("jishaku")

    async def on_ready(self):
        currUser = None if self.user is None else self.user.name
        self.logger.info(f"{currUser} is fully ready!")
