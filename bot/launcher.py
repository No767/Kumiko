import os
import signal
from pathlib import Path

import asyncpg
import discord
from aiohttp import ClientSession
from kumiko import Kumiko, init
from libs.utils import KumikoConfig, KumikoLogger
from libs.utils.handler import KeyboardInterruptHandler

if os.name == "nt":
    from winloop import run
else:
    from uvloop import run

config_path = Path(__file__).parent / "config.yml"
config = KumikoConfig(config_path)


TOKEN = config["kumiko"]["token"]
POSTGRES_URI = config["postgres_uri"]

intents = discord.Intents.default()
intents.message_content = True


async def main() -> None:
    async with (
        ClientSession() as session,
        asyncpg.create_pool(
            dsn=POSTGRES_URI,
            command_timeout=30,
            max_size=25,
            min_size=25,
            init=init,
        ) as pool,
    ):
        async with Kumiko(
            config=config,
            intents=intents,
            session=session,
            pool=pool,
        ) as bot:
            bot.loop.add_signal_handler(signal.SIGTERM, KeyboardInterruptHandler(bot))
            bot.loop.add_signal_handler(signal.SIGINT, KeyboardInterruptHandler(bot))
            await bot.start(TOKEN)


def launch() -> None:
    with KumikoLogger():
        run(main())


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
