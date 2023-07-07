import sys
import uuid
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
    assert (res == DATA.encode("utf-8")) and (isinstance(res, bytes))  # nosec


@pytest.mark.asyncio
async def test_json_cache():
    key = CommandKeyBuilder(id=uuid.uuid4(), command=None)
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


@pytest.mark.asyncio
async def test_get_json_cache_if_none():
    key = CommandKeyBuilder(id=123564343, command="ayo_what_mate")
    connPool = ConnectionPool().from_url("redis://localhost:6379/0")
    cache = KumikoCache(connection_pool=connPool)
    res = await cache.getJSONCache(key=key)
    assert res is None
