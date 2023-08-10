import sys
import uuid
from pathlib import Path

import pytest
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import CommandKeyBuilder, KumikoCache

DATA = "Hello World"
DICT_DATA = {"message": DATA}
OTHER_DATA = {"no": "yes"}

REDIS_URI = "redis://localhost:6379/0"


@pytest.mark.asyncio
async def test_basic_cache():
    key = CommandKeyBuilder(id=None, command=None)
    connPool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=connPool)
    await cache.setBasicCache(key=key, value=DATA)
    res = await cache.getBasicCache(key=key)
    assert (res == DATA.encode("utf-8")) and (isinstance(res, bytes))  # nosec


@pytest.mark.asyncio
async def test_json_cache():
    key = CommandKeyBuilder(id=uuid.uuid4(), command=None)
    connPool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=connPool)
    await cache.setJSONCache(key=key, value=DICT_DATA)
    res = await cache.getJSONCache(key=key, path=".")
    assert (res == DICT_DATA) and (isinstance(res, dict))  # nosec


@pytest.mark.asyncio
async def test_key_exists():
    key = CommandKeyBuilder(id=12352, command=None)
    connPool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=connPool)
    await cache.setBasicCache(key=key, value=DATA)
    res = await cache.cacheExists(key=key)
    assert res is True  # nosec


@pytest.mark.asyncio
async def test_get_json_cache_if_none():
    key = CommandKeyBuilder(id=123564343, command="ayo_what_mate")
    connPool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=connPool)
    res = await cache.getJSONCache(key=key)
    assert res is None


@pytest.mark.asyncio
async def test_delete_json_cache():
    key = CommandKeyBuilder(id=123564343453453, command="nicer")
    connPool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=connPool)
    await cache.setJSONCache(key=key, value=DATA)
    await cache.deleteJSONCache(key=key)
    res = await cache.cacheExists(key=key)
    assert res is False


@pytest.mark.asyncio
async def test_merge_json_cache_no_ttl():
    key = "cache:213423425:cache"
    cache = KumikoCache(connection_pool=ConnectionPool().from_url(REDIS_URI))
    await cache.mergeJSONCache(key=key, path="$", value=DICT_DATA, ttl=None)
    res = await cache.getJSONCache(key=key)
    assert isinstance(res, dict) and res == DICT_DATA


@pytest.mark.asyncio
async def test_merge_json_cache_with_ttl():
    FULL_DATA = {"message": DATA, "testing": "no"}
    key = "cache:21342342523423424:cache"
    cache = KumikoCache(connection_pool=ConnectionPool().from_url(REDIS_URI))
    await cache.mergeJSONCache(key=key, path="$", value=DICT_DATA, ttl=60)
    await cache.mergeJSONCache(key=key, path="$.testing", value="no", ttl=60)
    res = await cache.getJSONCache(key=key)
    assert res == FULL_DATA and isinstance(res, dict)


@pytest.mark.asyncio
async def test_get_json_list():
    key = "cache:2134234252342342423424:cache"
    cache = KumikoCache(connection_pool=ConnectionPool().from_url(REDIS_URI))
    await cache.setJSONCache(key=key, path="$", value=DATA, ttl=None)
    res = await cache.getJSONCache(key=key, value_only=False)
    assert isinstance(res, list)
