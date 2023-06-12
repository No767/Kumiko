import os

import discord
from aiohttp import ClientSession
from anyio import run
from dotenv import load_dotenv
from kumikocore import KumikoCore
from Libs.utils.postgresql import PrismaSessionManager
from Libs.utils import KumikoLogger

load_dotenv()

KUMIKO_TOKEN = os.environ["DEV_BOT_TOKEN"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")
intents = discord.Intents.default()
intents.message_content = True



async def main() -> None:
    async with ClientSession() as session:
        async with KumikoCore(
            intents=intents,
            session=session,
            dev_mode=DEV_MODE,
        ) as bot:
            await bot.start(KUMIKO_TOKEN)


def launch() -> None:
    with PrismaSessionManager():
        run(main, backend_options={"use_uvloop": True})


if __name__ == "__main__":
    try:
        with KumikoLogger():
            launch()
    except KeyboardInterrupt:
        pass
