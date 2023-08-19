import asyncio
import os

import asyncpg
import discord
from aiohttp import ClientSession
from dotenv import load_dotenv
from kumikocore import KumikoCore
from Libs.cache import KumikoCPManager
from Libs.utils import KumikoLogger, setup_ssl

# Only used for Windows development
if os.name == "nt":
    import winloop

    asyncio.set_event_loop_policy(winloop.WinLoopPolicy())
else:
    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

load_dotenv()

KUMIKO_TOKEN = os.environ["KUMIKO_TOKEN"]
DEV_MODE = os.getenv("DEV_MODE") in ("True", "TRUE")
SSL = os.getenv("SSL") in ("True", "TRUE")
SSL_CA = os.getenv("SSL_CA")
SSL_CERT = os.environ["SSL_CERT"]
SSL_KEY = os.getenv("SSL_KEY")
SSL_KEY_PASSWORD = os.getenv("SSL_KEY_PASSWORD")
POSTGRES_URI = os.environ["POSTGRES_URI"]
REDIS_URI = os.environ["REDIS_URI"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


async def main() -> None:
    async with ClientSession() as session, asyncpg.create_pool(
        dsn=POSTGRES_URI,
        command_timeout=60,
        max_size=25,
        min_size=25,
        ssl=setup_ssl(
            ca_path=SSL_CA,
            cert_path=SSL_CERT,
            key_path=SSL_KEY,
            key_password=SSL_KEY_PASSWORD,
        )
        if SSL is True
        else None,
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


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
