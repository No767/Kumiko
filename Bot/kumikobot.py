import logging
import os

import discord
from anyio import run
from dotenv import load_dotenv
from kumikocore import KumikoCore

load_dotenv()

KUMIKO_TOKEN = os.environ["DEV_BOT_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

FORMATTER = logging.Formatter(
    fmt="%(asctime)s %(levelname)s    %(message)s", datefmt="[%Y-%m-%d %H:%M:%S]"
)
discord.utils.setup_logging(formatter=FORMATTER)

logger = logging.getLogger("discord")
logging.getLogger("gql").setLevel(logging.WARNING)


async def main() -> None:
    async with KumikoCore(intents=intents) as bot:
        await bot.start(KUMIKO_TOKEN)


if __name__ == "__main__":
    try:
        run(main, backend_options={"use_uvloop": True})
    except KeyboardInterrupt:
        logger.info("Shutting down...")
