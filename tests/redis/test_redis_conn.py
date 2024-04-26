import sys
from pathlib import Path

import pytest
from redis.asyncio.connection import ConnectionPool

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from libs.utils import ensure_redis_conn


@pytest.mark.asyncio
async def test_open_conn():
    pool = ConnectionPool().from_url("redis://localhost:6379/0")
    res = await ensure_redis_conn(redis_pool=pool)
    assert res is True  # nosec
