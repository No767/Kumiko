import logging
from types import TracebackType
from typing import Optional, Type, TypeVar

from prisma import Prisma
from prisma.utils import async_run

BE = TypeVar("BE", bound=BaseException)

logger = logging.getLogger("discord") or logging.getLogger(__name__)


class PrismaSessionManager:
    """Context manager for managing Prisma Sessions"""

    def __init__(self) -> None:
        self.self = self
        self.db = Prisma(auto_register=True)

    def __enter__(self) -> None:
        async_run(self.db.connect())
        logger.info("Successfully connected to PostgreSQL database")

    def __exit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        if self.db.is_connected() is True:
            async_run(self.db.disconnect())
            logging.info("Safely disconnected from PostgreSQL database")
