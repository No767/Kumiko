import sys
from pathlib import Path

import pytest
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import set_or_update_cache


@pytest.fixture(scope="session")
def get_data():
    return {"id": 123, "channel_id": 2342634575000}


@pytest.mark.asyncio
async def test_set_or_update_cache(get_data):
    conn_pool = ConnectionPool()
    key = "cache:kumiko:123:config"
    cache = KumikoCache(conn_pool)
    await set_or_update_cache(key=key, redis_pool=conn_pool, data=get_data)
    res = await cache.get_json_cache(key=key)
    assert res == get_data


@pytest.mark.asyncio
async def test_cached_set_or_update(get_data):
    conn_pool = ConnectionPool()
    key = "cache:kumiko:1234:config"
    cache = KumikoCache(conn_pool)
    await cache.set_json_cache(key=key, value=get_data)
    await set_or_update_cache(key=key, redis_pool=conn_pool, data=get_data)
    res = await cache.get_json_cache(key=key)
    assert res == get_data and res["channel_id"] == get_data["channel_id"]  # type: ignore
