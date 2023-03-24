import logging

import discord
from anyio import Path
from discord.ext import commands
from Libs.utils.help import KumikoHelp
from Libs.utils.redis import redisCheck


class KumikoCore(commands.Bot):
    """The core of Kumiko - Subclassed this time"""

    def __init__(
        self,
        intents: discord.Intents,
        command_prefix: str = "?k ",
        redis_host: str = "localhost",
        redis_port: int = 6379,
        *args,
        **kwargs,
    ):
        super().__init__(
            intents=intents,
            command_prefix=command_prefix,
            help_command=KumikoHelp(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help"),
            *args,
            **kwargs,
        )
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.logger = logging.getLogger("kumikobot")

    async def setup_hook(self) -> None:
        cogsPath = Path(__file__).parent.joinpath("Cogs")
        async for cog in cogsPath.rglob("**/*.py"):
            if cog.parent.name == "Cogs":
                self.logger.debug(f"Loaded Cog: {cog.parent.name}.{cog.name[:-3]}")
                await self.load_extension(f"{cog.parent.name}.{cog.name[:-3]}")
            else:
                self.logger.debug(f"Loaded Cog: Cogs.{cog.parent.name}.{cog.name[:-3]}")
                await self.load_extension(f"Cogs.{cog.parent.name}.{cog.name[:-3]}")

        self.loop.create_task(redisCheck(self.redis_host, self.redis_port))

    async def on_ready(self):
        currUser = None if self.user is None else self.user.name
        self.logger.info(f"{currUser} is fully ready!")
