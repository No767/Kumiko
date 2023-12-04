import os
import sys
from pathlib import Path

import asyncpg
import pytest
import pytest_asyncio
from dotenv import load_dotenv

another_path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(another_path))


from Libs.utils.blacklist import BlacklistEntity, get_blacklist

load_dotenv(dotenv_path=another_path.joinpath(".env"))

POSTGRES_URI = os.environ["POSTGRES_URI"]


@pytest_asyncio.fixture
async def setup():
    async with asyncpg.create_pool(dsn=POSTGRES_URI) as pool:
        yield pool


def test_blacklist_entity():
    record = {"id": 3, "blacklist_status": False}
    first_entity = BlacklistEntity(record=record)
    assert first_entity.id == 3 and first_entity.blacklist_status is False

    second_entity = BlacklistEntity()
    assert second_entity.blacklist_status is None


@pytest.mark.asyncio
async def test_get_blacklist(setup):
    unknown_call = await get_blacklist(3, setup)
    assert unknown_call.blacklist_status is None

    query = """
    INSERT INTO blacklist (id, blacklist_status)
    VALUES ($1, $2) ON CONFLICT (id) DO NOTHING;
    """

    known_id = 1234567890
    await setup.execute(query, known_id, True)

    known_call = await get_blacklist(known_id, setup)
    assert known_call.id == known_id and known_call.blacklist_status is True
