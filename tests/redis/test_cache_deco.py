import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import cache, cacheJson
from redis.asyncio.connection import ConnectionPool


@pytest.mark.asyncio
async def test_cache_deco():
    connPool = ConnectionPool(max_connections=25)

    @cache(connection_pool=connPool)
    async def testFunc(id=1235):
        return "Hello World"

    res = await testFunc(1235)
    assert (await testFunc(1235) == "Hello World".encode("utf-8")) and isinstance(
        res, str
    )  # nosec


@pytest.mark.asyncio
async def test_cache_deco_json():
    connPool = ConnectionPool(max_connections=25)

    @cacheJson(connection_pool=connPool)
    async def testFuncJSON(id=182348478):
        return {"message": "Hello World"}

    res = await testFuncJSON(182348478)
    assert (
        await testFuncJSON(182348478) == {"message": "Hello World"}
    ) and isinstance(  # nosec
        res, dict
    )
