import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List

import discord
from aiocache import Cache
from coredis.exceptions import ConnectionError
from discord.ext import ipc, tasks
from discord.ext.ipc.objects import ClientPayload
from discord.ext.ipc.server import Server
from Libs.kumiko_utils import backoff
from Libs.kumiko_utils.postgresql import connectPostgres
from Libs.kumiko_utils.redis import pingRedisServer, setupRedisConnPool

path = Path(__file__).parents[0].absolute()
cogsPath = os.path.join(str(path), "Cogs")
libsPath = os.path.join(str(path), "Libs")
sys.path.append(libsPath)


class KumikoCore(discord.Bot):
    """The core of Kumiko - Subclassed this time"""

    def __init__(
        self,
        uri: str,
        models: List,
        redis_host: str,
        redis_port: int,
        ipc_secret_key: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.models = models
        self.ipc_secret_key = ipc_secret_key
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.backoffSec = 15
        self.backoffSecIndex = 0
        self.databaseBackoffSec = 15
        self.databaseBackoffSecIndex = 0
        self.ipcStarted = asyncio.Event()
        self.ipc = ipc.Server(self, secret_key=self.ipc_secret_key)
        self.loop.create_task(self.redisCheck())
        self.loop.create_task(self.connPostgres())
        self.startIPCServer.start()
        self.logger = logging.getLogger("kumikobot")
        self.load_cogs()

    def load_cogs(self):
        """Kumiko's system to load cogs"""
        cogsPath = Path(__file__).parent.joinpath("Cogs")
        for cog in cogsPath.rglob("**/*.py"):
            if cog.parent.name == "Cogs":
                self.logger.debug(f"Loaded Cog: {cog.parent.name}.{cog.name[:-3]}")
                self.load_extension(f"{cog.parent.name}.{cog.name[:-3]}")
            else:
                self.logger.debug(f"Loaded Cog: Cogs.{cog.parent.name}.{cog.name[:-3]}")
                self.load_extension(f"Cogs.{cog.parent.name}.{cog.name[:-3]}")

    async def redisCheck(self) -> None:
        try:
            memCache = Cache()
            await setupRedisConnPool()
            res = await pingRedisServer(connection_pool=await memCache.get(key="main"))
            if res is True:
                self.logger.info("Successfully connected to Redis server")
        except (ConnectionError, TimeoutError):
            backOffTime = backoff(
                backoff_sec=self.backoffSec, backoff_sec_index=self.backoffSecIndex
            )
            self.logger.error(
                f"Failed to connect to Redis server - Reconnecting in {int(backOffTime)} seconds"
            )
            await asyncio.sleep(backOffTime)
            self.backoffSecIndex += 1
            await self.redisCheck()

    async def connPostgres(self) -> None:
        try:
            await connectPostgres(uri=self.uri, models=self.models)
            self.logger.info("Successfully connected to PostgreSQL server")
        except TimeoutError:
            backOffTime = backoff(
                backoff_sec=self.databaseBackoffSec,
                backoff_sec_index=self.databaseBackoffSecIndex,
            )
            self.logger.error(
                f"Failed to connect to PostgreSQL server - Reconnecting in {int(backOffTime)} seconds"
            )
            await asyncio.sleep(backOffTime)
            self.databaseBackoffSecIndex += 1
            await self.connPostgres()

    @tasks.loop(hours=1)
    async def checkerHandler(self):
        self.logger.info("Tasks Disabled")
        # await QuestsChecker(uri=self.uri)
        # await AHChecker(uri=self.uri)

    @checkerHandler.before_loop
    async def beforeReady(self):
        await self.wait_until_ready()

    @checkerHandler.error
    async def checkHandlerError(self):
        self.logger.error(
            f"{self.user.name}'s Checker Handlers has failed. Attempting to restart"
        )
        await asyncio.sleep(5)
        self.checkerHandler.restart()

    @checkerHandler.after_loop
    async def afterReady(self):
        if self.checkerHandler.is_being_cancelled():
            self.checkerHandler.stop()

    @tasks.loop(count=1)
    async def startIPCServer(self):
        await self.ipc.start()
        self.ipcStarted.set()

    @startIPCServer.after_loop
    async def ipcTeardown(self):
        if self.startIPCServer.is_being_cancelled():
            await self.ipc.stop()
            self.ipcStarted.clear()

    @Server.route()
    async def get_user_data(self, data: ClientPayload) -> Dict:
        user = self.get_user(data.user_id)
        return user._to_minimal_user_json()

    @Server.route()
    async def create_embed(self, data: ClientPayload) -> None:
        print(data.embed_content)
        self.logger.info(f"Embed created, and sent to {data.channel_id}")

    async def on_ready(self):
        self.logger.info(f"{self.user.name} is fully ready!")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
        )
