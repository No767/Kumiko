import logging
import os
import sys
from pathlib import Path
from typing import Dict

import discord
from discord.ext import ipc, tasks
from discord.ext.ipc.objects import ClientPayload
from discord.ext.ipc.server import Server
from kumiko_economy_utils import AHChecker, QuestsChecker

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

    def __init__(self, uri: str, ipc_secret_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uri = uri
        self.ipc_secret_key = ipc_secret_key
        self.ipc = ipc.Server(self, secret_key=self.ipc_secret_key)
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
        await QuestsChecker(uri=self.uri)
        await AHChecker(uri=self.uri)

    @checkerHandler.before_loop
    async def beforeReady(self):
        await self.wait_until_ready()

    @checkerHandler.after_loop
    async def afterReady(self):
        if self.checkerHandler.failed():
            logging.error(
                f"{self.user.name}'s Checker Handlers has failed. Attempting to restart"
            )
            self.checkerHandler.restart()
        elif self.checkerHandler.is_being_cancelled():
            logging.info(f"Stopping {self.user.name}'s Checker Handlers")
            self.checkerHandler.stop()

    @Server.route()
    async def get_user_data(self, data: ClientPayload) -> Dict:
        user = self.get_user(data.user_id)
        return user._to_minimal_user_json()

    @Server.route()
    async def create_embed(self, data: ClientPayload) -> None:
        print(data.embed_content)
        logging.debug(f"Embed created, and sent to {data.channel_id}")

    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name}")
        self.checkerHandler.start()
        logging.info(f"{self.user.name}'s Checker Handlers successfully started")
        logging.info(f"Loaded all checkers")
        await self.ipc.start()
        logging.info(f"{self.user.name} is ready")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
        )
