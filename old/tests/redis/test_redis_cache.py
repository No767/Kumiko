import sys
import uuid
from pathlib import Path

import pytest
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from libs.cache import KumikoCache, command_key_builder

DATA = "Hello World"
DICT_DATA = {"message": DATA}
OTHER_DATA = {"no": "yes"}
FULL_DATA = {"message": DATA, "testing": "no"}

REDIS_URI = "redis://localhost:6379/0"


@pytest.mark.asyncio
async def test_basic_cache():
    key = command_key_builder(id=None, command=None)
    conn_pool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=conn_pool)
    await cache.set_basic_cache(key=key, value=DATA)
    res = await cache.get_basic_cache(key=key)
    assert (res == DATA.encode("utf-8")) and (isinstance(res, bytes))  # nosec


@pytest.mark.asyncio
async def test_json_cache():
    key = command_key_builder(id=uuid.uuid4(), command=None)
    conn_pool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=conn_pool)
    await cache.set_json_cache(key=key, value=DICT_DATA)
    res = await cache.get_json_cache(key=key, path=".")
    assert (res == DICT_DATA) and (isinstance(res, dict))  # nosec


@pytest.mark.asyncio
async def test_key_exists():
    key = command_key_builder(id=12352, command=None)
    conn_pool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=conn_pool)
    await cache.set_basic_cache(key=key, value=DATA)
    res = await cache.cache_exists(key=key)
    assert res is True  # nosec


@pytest.mark.asyncio
async def test_get_json_cache_if_none():
    key = command_key_builder(id=123564343, command="ayo_what_mate")
    conn_pool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=conn_pool)
    res = await cache.get_json_cache(key=key)
    assert res is None


@pytest.mark.asyncio
async def test_delete_json_cache():
    key = command_key_builder(id=123564343453453, command="nicer")
    conn_pool = ConnectionPool().from_url(REDIS_URI)
    cache = KumikoCache(connection_pool=conn_pool)
    await cache.set_json_cache(key=key, value=DATA)
    await cache.delete_json_cache(key=key)
    res = await cache.cache_exists(key=key)
    assert res is False


@pytest.mark.asyncio
async def test_merge_json_cache_no_ttl():
    key = "cache:213423425:cache"
    cache = KumikoCache(connection_pool=ConnectionPool().from_url(REDIS_URI))
    await cache.merge_json_cache(key=key, path="$", value=DICT_DATA, ttl=None)
    res = await cache.get_json_cache(key=key)
    assert isinstance(res, dict) and res == DICT_DATA


@pytest.mark.asyncio
async def test_merge_json_cache_with_ttl():
    key = "cache:21342342523423424:cache"
    cache = KumikoCache(connection_pool=ConnectionPool().from_url(REDIS_URI))
    await cache.merge_json_cache(key=key, path="$", value=DICT_DATA, ttl=60)
    await cache.merge_json_cache(key=key, path="$.testing", value="no", ttl=60)
    res = await cache.get_json_cache(key=key)
    assert res == FULL_DATA and isinstance(res, dict)


@pytest.mark.asyncio
async def test_get_json_list():
    key = "cache:2134234252342342423424:cache"
    cache = KumikoCache(connection_pool=ConnectionPool().from_url(REDIS_URI))
    await cache.set_json_cache(key=key, path="$", value=DATA, ttl=None)
    res = await cache.get_json_cache(key=key, value_only=False)
    assert isinstance(res, list)


@pytest.mark.asyncio
async def test_delete_basic_cache():
    key = "cache:99999999999999999999:cache"
    cache = KumikoCache(connection_pool=ConnectionPool().from_url(REDIS_URI))
    await cache.set_basic_cache(key=key, value="yo")
    await cache.delete_basic_cache(key=key)
    assert await cache.cache_exists(key) is False
