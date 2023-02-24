import os
import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "Bot", "Libs")
sys.path.append(packagePath)

CONNECTION_URI = "asyncpg://postgres:postgres@localhost:5432/postgres"
MODELS = [
    "kumiko_servers.models",
    "kumiko_economy.models",
]

from kumiko_utils.postgresql import connectPostgres


@pytest.mark.asyncio
async def test_postgres_conn():
    await connectPostgres(uri=CONNECTION_URI, models=MODELS)
    assert True  # nosec
