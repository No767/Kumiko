import asyncio
import os
from pathlib import Path

import asyncpg
import discord
from aiohttp import ClientSession
from kumikocore import KumikoCore
from Libs.cache import KumikoCPManager
from Libs.utils import KumikoConfig, KumikoLogger

if os.name == "nt":
    from winloop import install
else:
    from uvloop import install

CONFIG_PATH = Path(__file__).parent / "config.yml"
config = KumikoConfig(CONFIG_PATH)

TOKEN: str = config["kumiko"]["token"]
POSTGRES_URI = config["postgres_uri"]
REDIS_URI = config["redis_uri"]

intents = discord.Intents.default()
intents.message_content = True


async def main() -> None:
    async with ClientSession() as session, asyncpg.create_pool(
        dsn=POSTGRES_URI,
        command_timeout=30,
        max_size=25,
        min_size=25,
    ) as pool, KumikoCPManager(uri=REDIS_URI, max_size=25) as redis_pool:
        async with KumikoCore(
            config=config,
            intents=intents,
            session=session,
            pool=pool,
            redis_pool=redis_pool,
        ) as bot:
            await bot.start(TOKEN)


def launch() -> None:
    with KumikoLogger():
        install()
        asyncio.run(main())


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
