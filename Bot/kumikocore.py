import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import List

import discord
from discord.ext import ipc, tasks
from tortoise import Tortoise

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] | %(asctime)s >> %(message)s",
    datefmt="[%m/%d/%Y] [%I:%M:%S %p %Z]",
)

logging.getLogger("asyncio_redis").setLevel(logging.WARNING)
logging.getLogger("tortoise").setLevel(logging.WARNING)
logging.getLogger("gql").setLevel(logging.WARNING)

path = Path(__file__).parents[0].absolute()
cogsPath = os.path.join(str(path), "Cogs")
libsPath = os.path.join(str(path), "Libs")
sys.path.append(libsPath)


class KumikoCore(discord.Bot):
    """The core of Kumiko - Subclassed this time"""

    def __init__(self, uri: str, models: List, ipc_secret_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.models = models
        self.ipc_secret_key = ipc_secret_key
        self.dbConnected = asyncio.Event()
        self.ipc = ipc.Server(self, secret_key=self.ipc_secret_key)
        self.connectDB.add_exception_type(TimeoutError)
        self.connectDB.start()
        self.checkerHandler.start()
        self.load_cogs()

    def load_cogs(self):
        """Kumiko's system to load cogs"""
        cogsList = os.listdir(cogsPath)
        for cogDir in cogsList:
            if cogDir not in ["__pycache__"]:
                subCogsList = os.listdir(os.path.join(cogsPath, cogDir))
                for subCogDir in subCogsList:
                    if subCogDir not in [
                        "__pycache__",
                    ] and not subCogDir.endswith(".py"):
                        for lastCog in os.listdir(
                            os.path.join(cogsPath, cogDir, subCogDir)
                        ):
                            if lastCog not in ["__pycache__", "config"]:
                                logging.debug(
                                    f"Loaded Cog: Cogs.{cogDir}.{subCogDir}.{lastCog[:-3]}"
                                )
                                self.load_extension(
                                    f"Cogs.{cogDir}.{subCogDir}.{lastCog[:-3]}",
                                    store=False,
                                )
                    elif subCogDir.endswith(".py"):
                        logging.debug(f"Loaded Cog: Cogs.{cogDir}.{subCogDir[:-3]}")
                        self.load_extension(
                            f"Cogs.{cogDir}.{subCogDir[:-3]}", store=False
                        )

    @tasks.loop(hours=1)
    async def checkerHandler(self):
        logging.info("Tasks Disabled")
        # await QuestsChecker(uri=self.uri)
        # await AHChecker(uri=self.uri)

    @checkerHandler.before_loop
    async def beforeReady(self):
        await self.wait_until_ready()

    @checkerHandler.error
    async def checkHandlerError(self):
        logging.error(
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
        await Tortoise.init(db_url=self.uri, modules={"models": self.models})
        self.dbConnected.set()
        logging.info("Successfully connected to PostgreSQL")

    # Note that this reconnection logic does not work
    # Tortoise ORM's init coroutine does not raise an exception, but instead makes asyncpg do the dirty work
    # The exception should be TimeoutError, this can't be caught for some reason
    @connectDB.error
    async def connectDBError(self):
        logging.error("Failed to connect to PostgreSQL. Retrying in 5 seconds")
        await asyncio.sleep(5)
        await self.connectDB.restart()

    @connectDB.after_loop
    async def connectionTeardown(self):
        if self.connectDB.is_being_cancelled():
            await Tortoise.close_connections()
            self.dbConnected.clear()

    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name}")
        logging.info(f"{self.user.name} is ready")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
        )
