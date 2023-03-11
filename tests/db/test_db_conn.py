import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))


from Libs.utils.postgresql import connPostgres


@pytest.mark.asyncio
async def test_postgres_conn():
    await connPostgres()
    assert True  # nosec
