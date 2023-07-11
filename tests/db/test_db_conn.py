import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

load_dotenv()

import asyncpg
from Libs.utils.postgresql import ensureOpenPostgresConn


@pytest.fixture(scope="session")
def get_uri():
    pg_uri = os.getenv("POSTGRES_URI")
    if pg_uri is None:
        return "postgresql://postgres:postgres@localhost:5432/test"
    return pg_uri


@pytest.mark.asyncio
async def test_open_postgres_conn(get_uri):
    async with asyncpg.create_pool(dsn=get_uri) as pool:
        res = await ensureOpenPostgresConn(conn_pool=pool)
        assert res is True
