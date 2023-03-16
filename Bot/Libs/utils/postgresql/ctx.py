import logging
from contextlib import asynccontextmanager

from prisma import Prisma  # type: ignore
from prisma.engine.errors import EngineConnectionError  # type: ignore

logger = logging.getLogger("discord") or logging.getLogger(__name__)

# This will only really be kept around for either test scripts or for other purposes
@asynccontextmanager
async def PrismaClientSession():
    """Implements an asynchronous context manager for Prisma client sessions

    Raises:
        EngineConnectionError: Raised when the PostgreSQL server or DB server is unreachable

    Returns:
        AsyncIterator[None]: Returns an asynchronous context manager for Prisma client sessions
    """
    try:
        db = Prisma(auto_register=True)
        conn = await db.connect()
        logger.info("Successfully connected to PostgreSQL database")
        yield conn
    except EngineConnectionError:
        logger.error("Failed to connect to PostgreSQL database")
        raise EngineConnectionError
    finally:
        await db.disconnect()
