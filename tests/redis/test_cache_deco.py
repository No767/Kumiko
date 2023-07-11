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

    @cache()
    async def testFunc(
        id=1235, redis_pool=ConnectionPool.from_url("redis://localhost:6379/0")
    ):
        return "Hello World"

    res = await testFunc(1235, connPool)
    assert (
        await testFunc(1235, connPool) == "Hello World".encode("utf-8")
    ) and isinstance(
        res, str
    )  # nosec


@pytest.mark.asyncio
async def test_cache_deco_json():
    connPool = ConnectionPool(max_connections=25)

    @cacheJson()
    async def testFuncJSON(
        id=182348478, redis_pool=ConnectionPool.from_url("redis://localhost:6379/0")
    ):
        return {"message": "Hello World"}

    res = await testFuncJSON(182348478, connPool)
    assert (
        await testFuncJSON(182348478, connPool) == {"message": "Hello World"}
    ) and isinstance(  # nosec
        res, dict
    )


# the results of these should be the types returned
# within the decos, there is code that refuses to cache if the return type is not what is needed
@pytest.mark.asyncio
async def test_cache_deco_invalid():
    connPool = ConnectionPool()

    @cache()
    async def testFuncInvalid(id=2345973453, redis_pool=ConnectionPool()):
        return 23464354

    res = await testFuncInvalid(2345973453, connPool)
    assert await testFuncInvalid(2345973453, connPool) == 23464354 and isinstance(
        res, int
    )


@pytest.mark.asyncio
async def test_cache_deco_json_invalid():
    connPool = ConnectionPool()

    @cacheJson()
    async def testFuncJSONInvalid(id=2345973453, redis_pool=ConnectionPool()):
        return [1, 2, 3, 4, 5]

    res = await testFuncJSONInvalid(2345973453, connPool)
    assert 1 in res and isinstance(res, list)  # type: ignore
