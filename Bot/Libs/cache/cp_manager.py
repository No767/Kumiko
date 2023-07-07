from types import TracebackType
from typing import Optional, Type, TypeVar

from redis.asyncio.connection import ConnectionPool
from yarl import URL

BE = TypeVar("BE", bound=BaseException)


class KumikoCPManager:
    def __init__(self, uri: str, max_size: int = 20) -> None:
        self.uri = uri
        self.max_size = max_size
        self.connPool = None

    async def __aenter__(self) -> ConnectionPool:
        return self.createPool()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        if self.connPool is not None:
            await self.connPool.disconnect()

    def createPool(self) -> ConnectionPool:
        completeURI = URL(self.uri) % {"decode_responses": "True"}
        self.connPool = ConnectionPool(max_connections=self.max_size).from_url(
            str(completeURI)
        )
        return self.connPool

    def getConnPool(self) -> ConnectionPool:
        if not self.connPool:
            return self.createPool()
        return self.connPool
