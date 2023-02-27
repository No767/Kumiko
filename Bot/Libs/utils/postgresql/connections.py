import asyncio
import logging

from prisma import Prisma
from prisma.engine.errors import EngineConnectionError

from ..backoff import backoff

logger = logging.getLogger("discord")
backoffSec = 10
backoffSecIndex = 0


async def connPostgres() -> None:
    """Connects to the PostgreSQL database

    Args:
        uri (str): PostgreSQL Connection URI
    """
    try:
        db = Prisma(auto_register=True)
        await db.connect()
        logger.info("Successfully connected to PostgreSQL server")
    except EngineConnectionError:
        backoffTime = backoff(backoff_sec=backoffSec, backoff_sec_index=backoffSecIndex)
        logger.error(
            f"Failed to connect to PostgreSQL server - Restarting connection in {int(backoffTime)} seconds"
        )
        await asyncio.sleep(backoffTime)
        await connPostgres()
