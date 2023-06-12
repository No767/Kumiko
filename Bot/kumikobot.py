import os

import discord
from aiohttp import ClientSession
from anyio import run
from dotenv import load_dotenv
from kumikocore import KumikoCore
from Libs.utils import KumikoLogger
import asyncpg
load_dotenv()

KUMIKO_TOKEN = os.environ["DEV_BOT_TOKEN"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")
POSTGRES_URI = os.environ["POSTGRES_URI"]

intents = discord.Intents.default()
intents.message_content = True



async def main() -> None:
    async with ClientSession() as session, asyncpg.create_pool(dsn=POSTGRES_URI, command_timeout=60, max_size=20, min_size=20) as pool:
        async with KumikoCore(
            intents=intents,
            session=session,
            pool=pool,
            dev_mode=DEV_MODE,
        ) as bot:
            await bot.start(KUMIKO_TOKEN)


def launch() -> None:
    with KumikoLogger():
        run(main, backend_options={"use_uvloop": True})


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
