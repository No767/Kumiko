import logging
import os

import discord
from aiohttp import ClientSession
from anyio import run
from dotenv import load_dotenv
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from kumikocore import KumikoCore

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
    async with ClientSession() as session:
        async with Client(
            transport=AIOHTTPTransport(url="https://graphql.anilist.co/"),
            fetch_schema_from_transport=True,
        ) as gql_session:
            async with KumikoCore(
                intents=intents,
                session=session,
                gql_session=gql_session,
                dev_mode=DEV_MODE,
            ) as bot:
                await bot.start(KUMIKO_TOKEN)


if __name__ == "__main__":
    try:
        run(main, backend_options={"use_uvloop": True})
    except KeyboardInterrupt:
        logger.info("Shutting down...")
