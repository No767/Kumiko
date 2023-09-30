from typing import Optional

import asyncpg


class MaybeAcquireConnection:
    def __init__(
        self, connection: Optional[asyncpg.Connection], *, pool: asyncpg.Pool
    ) -> None:
        self._connection: Optional[asyncpg.Connection] = connection
        self.pool: asyncpg.Pool = pool
        self._cleanup: bool = False

    async def __aenter__(self) -> asyncpg.Connection:
        if self._connection is None:
            self._cleanup = True
            self._connection = c = await self.pool.acquire()
            return c
        return self._connection

    async def __aexit__(self, *args) -> None:
        if self._cleanup:
            await self.pool.release(self._connection)
