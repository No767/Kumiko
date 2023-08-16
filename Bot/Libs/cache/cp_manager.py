from types import TracebackType
from typing import Optional, Type, TypeVar

from redis.asyncio.connection import ConnectionPool
from yarl import URL

BE = TypeVar("BE", bound=BaseException)


class KumikoCPManager:
    def __init__(self, uri: str, max_size: int = 20) -> None:
        self.uri = uri
        self.max_size = max_size
        self.pool = None

    async def __aenter__(self) -> ConnectionPool:
        return self.create_pool()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        if self.pool is not None:
            await self.pool.disconnect()

    def create_pool(self) -> ConnectionPool:
        complete_uri = URL(self.uri) % {"decode_responses": "True", "protocol": 3}
        self.pool = ConnectionPool(max_connections=self.max_size).from_url(
            str(complete_uri)
        )
        return self.pool

    def get_conn_pool(self) -> ConnectionPool:
        if not self.pool:
            return self.create_pool()
        return self.pool
