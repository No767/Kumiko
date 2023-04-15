import logging
from pathlib import Path as SyncPath
from typing import Union

import discord
from aiohttp import ClientSession
from anyio import Path
from discord.ext import commands
from gql.client import AsyncClientSession, ReconnectingAsyncClientSession
from Libs.utils.help import KumikoHelpPaginated
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
        session: ClientSession,
        gql_session: Union[ReconnectingAsyncClientSession, AsyncClientSession],
        dev_mode: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned_or(">"),
            help_command=KumikoHelpPaginated(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help"),
            *args,
            **kwargs,
        )
        self.dev_mode = dev_mode
        self._session = session
        self._gql_session = gql_session
        self.logger: logging.Logger = logging.getLogger("kumikobot")

    @property
    def session(self) -> ClientSession:
        """A global web session used throughout the lifetime of the bot

        Returns:
            ClientSession: AIOHTTP's ClientSession
        """
        return self._session

    @property
    def gql_session(self) -> Union[ReconnectingAsyncClientSession, AsyncClientSession]:
        """A global GraphQL session used throughout the lifetime of the bot

        This is exclusively used for the AniList integration, thus the URL is set to the AniList GraphQL endpoints.

        Returns:
            Union[ReconnectingAsyncClientSession, AsyncClientSession]: The current GQL session
        """
        return self._gql_session

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
