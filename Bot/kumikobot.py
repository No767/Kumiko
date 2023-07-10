import asyncio
import os

import asyncpg
import discord
from aiohttp import ClientSession
from dotenv import load_dotenv
from kumikocore import KumikoCore
from Libs.cache import KumikoCPManager
from Libs.utils import KumikoLogger

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

load_dotenv()

KUMIKO_TOKEN = os.environ["DEV_BOT_TOKEN"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")
POSTGRES_URI = os.environ["POSTGRES_URI"]
REDIS_URI = os.environ["REDIS_URI"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


async def main() -> None:
    async with ClientSession() as session, asyncpg.create_pool(
        dsn=POSTGRES_URI, command_timeout=60, max_size=20, min_size=20
    ) as pool, KumikoCPManager(uri=REDIS_URI, max_size=25) as redis_pool:
        async with KumikoCore(
            intents=intents,
            session=session,
            pool=pool,
            redis_pool=redis_pool,
            dev_mode=DEV_MODE,
        ) as bot:
            await bot.start(KUMIKO_TOKEN)


def launch() -> None:
    with KumikoLogger():
        asyncio.run(main())
        # run(main, backend_options={"use_uvloop": True})


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
