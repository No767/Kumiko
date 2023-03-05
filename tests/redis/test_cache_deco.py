import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import cached
from redis.asyncio.connection import ConnectionPool


@pytest.mark.asyncio
async def test_cache_deco():
    connPool = ConnectionPool(max_connections=25)

    @cached(connection_pool=connPool, command_key=None)
    async def testFunc():
        return "Hello World"

    res = await testFunc()
    assert (await testFunc() == "Hello World") and isinstance(res, str)  # nosec
