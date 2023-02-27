import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import tasks
from Libs.utils.postgresql import connPostgres
from Libs.utils.redis import redisCheck


class KumikoCore(discord.Bot):
    """The core of Kumiko - Subclassed this time"""

    def __init__(
        self,
        redis_host: str,
        redis_port: int,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.loop.create_task(connPostgres())
        self.loop.create_task(redisCheck(redis_host, redis_port))
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

    async def on_ready(self):
        self.logger.info(f"{self.user.name} is fully ready!")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
        )
