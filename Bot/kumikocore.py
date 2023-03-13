import logging
from typing import Optional

import discord
from anyio import Path
from discord.ext import commands
from Libs.utils.redis import redisCheck


class KumikoCore(commands.Bot):
    """The core of Kumiko - Subclassed this time"""

    def __init__(
        self,
        intents: discord.Intents,
        command_prefix: str = "?k ",
        redis_host: str = "localhost",
        redis_port: int = 6379,
        testing_guild_id: Optional[int] = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            intents=intents,
            command_prefix=command_prefix,
            help_command=commands.DefaultHelpCommand(),
            activity=discord.Activity(type=discord.ActivityType.watching, name="/help"),
            *args,
            **kwargs,
        )
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.testing_guild_id = testing_guild_id
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

        # if self.testing_guild_id:
        #     guild = discord.Object(self.testing_guild_id)
        #     self.tree.copy_global_to(guild=guild)
        #     await self.tree.sync(guild=guild)

    async def on_ready(self):
        self.logger.info(f"{self.user.name} is fully ready!")
