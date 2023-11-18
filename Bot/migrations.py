import asyncio
import logging
import os
from pathlib import Path

import asyncpg
from asyncpg_trek import Direction, execute, plan
from asyncpg_trek.asyncpg import AsyncpgBackend
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
MIGRATIONS_DIR = ROOT_DIR / "Migrations"
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


POSTGRES_URI = os.environ["POSTGRES_URI"]
TARGET_REVISION = os.environ["TARGET_REVISION"]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Migrations] %(levelname)s\t%(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
)


async def migrate(
    conn: asyncpg.Connection,
    target_revision: str,
) -> None:
    backend = AsyncpgBackend(conn)
    async with backend.connect():
        planned = await plan(
            backend,
            MIGRATIONS_DIR,
            target_revision=target_revision,
            direction=Direction.up,
        )
        await execute(backend, planned)


async def main():
    conn = await asyncpg.connect(dsn=POSTGRES_URI)
    await migrate(conn, TARGET_REVISION)
    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
