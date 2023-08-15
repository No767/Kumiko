import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import cache, cache_json
from redis.asyncio.connection import ConnectionPool

DATA = "Hello World"

REDIS_URI = "redis://localhost:6379/0"


@pytest.mark.asyncio
async def test_cache_deco():
    conn_pool = ConnectionPool(max_connections=25)

    @cache()
    async def test_func(id=1235, redis_pool=ConnectionPool.from_url(REDIS_URI)):
        return DATA

    res = await test_func(1235, conn_pool)
    assert isinstance(res, str) or isinstance(res, bytes)


@pytest.mark.asyncio
async def test_cache_deco_caching():
    conn_pool = ConnectionPool(max_connections=25)

    @cache()
    async def test_func(id=1235, redis_pool=ConnectionPool.from_url(REDIS_URI)):
        return DATA

    res = await test_func(1235, conn_pool)
    res2 = await test_func(1235, conn_pool)
    assert (isinstance(res, str) or isinstance(res, bytes)) and (
        isinstance(res2, str) or isinstance(res2, bytes)
    )


@pytest.mark.asyncio
async def test_cache_deco_json():
    conn_pool = ConnectionPool(max_connections=25)

    @cache_json(path=".")
    async def test_func_json(
        id=182348478, redis_pool=ConnectionPool.from_url(REDIS_URI)
    ):
        return {"message": DATA}

    res = await test_func_json(182348478, conn_pool)
    assert (
        await test_func_json(182348478, conn_pool) == {"message": DATA}
    ) and isinstance(  # nosec
        res, dict
    )


# the results of these should be the types returned
# within the decos, there is code that refuses to cache if the return type is not what is needed
@pytest.mark.asyncio
async def test_cache_deco_invalid():
    conn_pool = ConnectionPool()

    @cache()
    async def test_func_invalid(id=2345973453, redis_pool=ConnectionPool()):
        return 23464354

    res = await test_func_invalid(2345973453, conn_pool)
    assert await test_func_invalid(2345973453, conn_pool) == 23464354 and isinstance(
        res, int
    )


@pytest.mark.asyncio
async def test_cache_deco_json_invalid():
    conn_pool = ConnectionPool()

    @cache_json()
    async def test_func_json_invalid(id=2345973453, redis_pool=ConnectionPool()):
        return [1, 2, 3, 4, 5]

    res = await test_func_json_invalid(2345973453, conn_pool)
    assert 1 in res and isinstance(res, list)  # type: ignore
