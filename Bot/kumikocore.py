import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List

import discord
from coredis import ConnectionPool
from coredis.exceptions import ConnectionError
from discord.ext import ipc, tasks
from discord.ext.ipc.objects import ClientPayload
from discord.ext.ipc.server import Server
from tortoise import BaseDBAsyncClient, Tortoise, connections
from tortoise.exceptions import DBConnectionError

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
        self.dbConnected = asyncio.Event()
        self.connPoolRedisSet = asyncio.Event()
        self.redisConnPool = ConnectionPool.from_url(
            url=f"redis://{self.redis_host}@:{self.redis_port}/0"
        )
        self.ipcStarted = asyncio.Event()
        self.ipc = ipc.Server(self, secret_key=self.ipc_secret_key)
        self.connectDB.add_exception_type(TimeoutError)
        self.connectDB.add_exception_type(DBConnectionError)
        self.startIPCServer.start()
        self.connectDB.start()
        self.connPoolRedis.start()
        self.checkerHandler.start()
        self.logger = logging.getLogger("kumikobot")
        self.load_cogs()

    def load_cogs(self):
        """Kumiko's system to load cogs"""
        cogsPath = Path(__file__).parent.joinpath("Cogs")
        for cog in cogsPath.rglob("*.py"):
            relativeParentName = cog.parents[1].name
            parentName = cog.parent.name
            cogName = cog.name
            if relativeParentName != "Cogs":
                self.logger.debug(
                    f"Loaded Cog: Cogs.{relativeParentName}.{parentName}.{cogName}"
                )
                self.load_extension(f"Cogs.{relativeParentName}.{parentName}.{cogName}")
            else:
                self.logger.debug(
                    f"Loaded Cog: {relativeParentName}.{parentName}.{cogName}"
                )
                self.load_extension(f"{relativeParentName}.{parentName}.{cogName}")

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
    async def connectDB(self):
        try:
            # Apparently Tortoise's init method does not connect to the DB that well
            await Tortoise.init(db_url=self.uri, modules={"models": self.models})
            conn: BaseDBAsyncClient = connections.get("default")
            await conn.create_connection(with_db=True)
            self.dbConnected.set()
            self.logger.info("Successfully connected to PostgreSQL")
        except TimeoutError:
            self.logger.error("Failed to connect to PostgreSQL. Retrying in 15 seconds")
            await asyncio.sleep(15)
            self.connectDB.restart()

    @connectDB.after_loop
    async def connectionTeardown(self):
        if self.connectDB.is_being_cancelled():
            await connections.close_all()
            self.dbConnected.clear()

    @tasks.loop(count=1)
    async def connPoolRedis(self):
        try:
            await self.redisConnPool.get_connection()
            self.connPoolRedisSet.set()
            self.logger.info("Successfully connected to Redis")
        except ConnectionError:
            self.logger.error("Failed to connect to Redis. Retrying in 15 seconds")
            await asyncio.sleep(15)
            self.connPoolRedis.restart()

    @connPoolRedis.after_loop
    async def connPoolRelease(self):
        if self.connPoolRedis.is_being_cancelled():
            self.redisConnPool.disconnect()
            self.connPoolRedisSet.clear()

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
