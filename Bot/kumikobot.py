import asyncio
import os
from pathlib import Path

import asyncpg
import discord
from aiohttp import ClientSession
from dotenv import load_dotenv
from kumikocore import KumikoCore
from Libs.cache import KumikoCPManager
from Libs.utils import KumikoLogger, init_codecs, read_env

if os.name == "nt":
    from winloop import install
else:
    from uvloop import install

load_dotenv()

ENV_PATH = Path(__file__).parent / ".env"

KUMIKO_TOKEN = os.environ["KUMIKO_TOKEN"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")
IPC_SECRET_KEY = os.environ["IPC_SECRET_KEY"]
IPC_HOST = os.environ["IPC_HOST"]
POSTGRES_URI = os.environ["POSTGRES_URI"]
REDIS_URI = os.environ["REDIS_URI"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


async def main() -> None:
    async with ClientSession() as session, asyncpg.create_pool(
        dsn=POSTGRES_URI,
        command_timeout=30,
        max_size=25,
        min_size=25,
        init=init_codecs,
    ) as pool, KumikoCPManager(uri=REDIS_URI, max_size=25) as redis_pool:
        async with KumikoCore(
            intents=intents,
            config=read_env(ENV_PATH),
            session=session,
            pool=pool,
            redis_pool=redis_pool,
            ipc_secret_key=IPC_SECRET_KEY,
            ipc_host=IPC_HOST,
            dev_mode=DEV_MODE,
        ) as bot:
            await bot.start(KUMIKO_TOKEN)


def launch() -> None:
    with KumikoLogger():
        install()
        asyncio.run(main())


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
