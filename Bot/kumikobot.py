import logging
import os

import discord
from anyio import run
from dotenv import load_dotenv
from kumikocore import KumikoCore

load_dotenv()

KUMIKO_TOKEN = os.environ["DEV_BOT_TOKEN"]
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ["REDIS_PORT"]

intents = discord.Intents.default()
intents.message_content = True

FORMATTER = logging.Formatter(
    fmt="%(asctime)s %(levelname)s    %(message)s", datefmt="[%Y-%m-%d %H:%M:%S]"
)
discord.utils.setup_logging(formatter=FORMATTER)

logger = logging.getLogger("discord")
logging.getLogger("gql").setLevel(logging.WARNING)


async def main() -> None:
    async with KumikoCore(
        intents=intents,
        command_prefix="?k ",
        redis_host=REDIS_HOST,
        redis_port=int(REDIS_PORT),
    ) as bot:
        await bot.start(KUMIKO_TOKEN)


if __name__ == "__main__":
    try:
        run(main, backend_options={"use_uvloop": True})
    except KeyboardInterrupt:
        logger.info("Shutting down...")
