import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from prisma import Prisma
from prisma.engine.errors import EngineConnectionError

logger = logging.getLogger("discord") or logging.getLogger(__name__)


@asynccontextmanager
async def PrismaClientSession() -> AsyncIterator[None]:
    """Implements an asynchronous context manager for Prisma client sessions

    Raises:
        EngineConnectionError: Raised when the PostgreSQL server or DB server is unreachable

    Returns:
        AsyncIterator[None]: Returns an asynchronous context manager for Prisma client sessions
    """
    db = Prisma(auto_register=True)
    conn = await db.connect()
    try:
        yield conn
    except EngineConnectionError:
        logger.error("Failed to connect to PostgreSQL database")
        raise EngineConnectionError
    finally:
        await db.disconnect()
