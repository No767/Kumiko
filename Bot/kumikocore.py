import logging
import os
import sys
from pathlib import Path

import discord

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name}")
        logging.info(
            f"{self.user.name} is ready to go! All checkers are loaded and ready!"
        )
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
        )
