import asyncio
import contextlib
import logging
import os

import discord
from aiohttp import ClientSession
from anyio import run
from dotenv import load_dotenv
from kumikocore import KumikoCore
from Libs.utils.postgresql import PrismaSessionManager

load_dotenv()

KUMIKO_TOKEN = os.environ["DEV_BOT_TOKEN"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")
intents = discord.Intents.default()
intents.message_content = True

FORMATTER = logging.Formatter(
    fmt="%(asctime)s %(levelname)s    %(message)s", datefmt="[%Y-%m-%d %H:%M:%S]"
)
discord.utils.setup_logging(formatter=FORMATTER)

logger = logging.getLogger("discord")
logging.getLogger("gql").setLevel(logging.WARNING)


async def main() -> None:
    async with PrismaSessionManager():
        async with ClientSession() as session:
            async with KumikoCore(
                intents=intents,
                session=session,
                dev_mode=DEV_MODE,
            ) as bot:
                await bot.start(KUMIKO_TOKEN)


if __name__ == "__main__":
    # I hate having to do this, but it's the only way to not get AIOHTTP to throw an cancellederror on me
    with contextlib.suppress(asyncio.CancelledError):
        try:
            run(main, backend_options={"use_uvloop": True})
        except KeyboardInterrupt:
            logger.info("Shutting down...")
