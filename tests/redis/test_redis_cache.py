import sys
from pathlib import Path

import pytest
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import CommandKeyBuilder, KumikoCache

DATA = "Hello World"
DICT_DATA = {"message": "Hello World"}


@pytest.mark.asyncio
async def test_basic_cache():
    key = CommandKeyBuilder(id=None, command=None)
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    cache = KumikoCache(connection_pool=connPool)
    await cache.setBasicCache(key=key, value=DATA)
    res = await cache.getBasicCache(key=key)
    assert (res == DATA) and (isinstance(res, str))  # nosec


@pytest.mark.asyncio
async def test_json_cache():
    key = CommandKeyBuilder(id=None, command=None)
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    cache = KumikoCache(connection_pool=connPool)
    await cache.setJSONCache(key=key, value=DICT_DATA)
    res = await cache.getJSONCache(key=key)
    assert (res == DICT_DATA) and (isinstance(res, dict))  # nosec


@pytest.mark.asyncio
async def test_key_exists():
    key = CommandKeyBuilder(id=12352, command=None)
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    cache = KumikoCache(connection_pool=connPool)
    await cache.setBasicCache(key=key, value=DATA)
    res = await cache.cacheExists(key=key)
    assert res is True  # nosec
