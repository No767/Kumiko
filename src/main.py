import contextlib
import os
import signal

import asyncpg
from aiohttp import ClientSession

from core import Kumiko, find_config, init
from utils import KumikoConfig, KumikoLogger
from utils.handler import KeyboardInterruptHandler

if os.name == "nt":
    from winloop import run
else:
    from uvloop import run


config = KumikoConfig.load_from_file(find_config())


async def main() -> None:
    async with (
        ClientSession() as session,
        asyncpg.create_pool(
            dsn=config.postgres_uri,
            command_timeout=30,
            max_size=25,
            min_size=25,
            init=init,
        ) as pool,
        Kumiko(
            config=config,
            session=session,
            pool=pool,
        ) as bot,
    ):
        bot.loop.add_signal_handler(signal.SIGTERM, KeyboardInterruptHandler(bot))
        bot.loop.add_signal_handler(signal.SIGINT, KeyboardInterruptHandler(bot))
        await bot.start(config.token)


def launch() -> None:
    with KumikoLogger():
        run(main())


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        launch()
