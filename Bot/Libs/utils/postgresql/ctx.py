import logging
from types import TracebackType
from typing import Optional, Type, TypeVar

from prisma import Prisma  # type: ignore
from prisma.engine.errors import EngineConnectionError  # type: ignore

BE = TypeVar("BE", bound=BaseException)

logger = logging.getLogger("discord") or logging.getLogger(__name__)


class PrismaSessionManager:
    """Context manager for managing Prisma Sessions"""

    def __init__(self) -> None:
        self.self = self
        self.db = Prisma(auto_register=True)

    async def __aenter__(self) -> None:
        await self.db.connect()
        logger.info("Successfully connected to PostgreSQL database")

    async def __aexit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        if isinstance(exc, EngineConnectionError):
            logging.error(f"Failed to connect to PostgreSQL database - {str(exc)}")
        elif self.db.is_connected() is True:
            await self.db.disconnect()
            logging.info("Safely disconnected from PostgreSQL database")
