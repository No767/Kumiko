import asyncio
import logging

from discord.ext import commands, tasks
from Libs.utils import backoff
from prisma import Prisma
from prisma.engine.errors import EngineConnectionError


class PrismaClientSession(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.backoffSec = 10
        self.backoffSecIndex = 0
        self.db = Prisma(auto_register=True)
        self.logger = logging.getLogger("discord")

    async def cog_load(self):
        self.connect.start()

    async def cog_unload(self):
        try:
            await self.db.disconnect()
        except EngineConnectionError as e:
            self.logger.error(
                f"Failed to disconnect from PostgreSQL database - {str(e)}"
            )

    @tasks.loop(count=1)
    async def connect(self):
        await self.db.connect()
        self.logger.info("Successfully connected to PostgreSQL database")

    @connect.error
    async def connError(self, exc: Exception):
        backoffTime = backoff(
            backoff_sec=self.backoffSec, backoff_sec_index=self.backoffSecIndex
        )
        self.backoffSecIndex += 1
        self.logger.error(
            f"({str(exc.__class__.__name__)}) Failed to connect to PostgreSQL database - Reconnecting in {int(backoffTime)} seconds"
        )
        await asyncio.sleep(backoffTime)
        self.connect.restart()


async def setup(bot: commands.Bot):
    await bot.add_cog(PrismaClientSession(bot))
