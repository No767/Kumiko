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
        self.loop.create_task(connPostgres())
        self.loop.create_task(redisCheck(redis_host, redis_port))
        self.setupHandler.start()
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

    @tasks.loop(count=1)
    async def setupHandler(self):
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help")
        )

    @setupHandler.before_loop
    async def beforeReady(self):
        await self.wait_until_ready()

    async def on_ready(self):
        self.logger.info(f"{self.user.name} is fully ready!")
