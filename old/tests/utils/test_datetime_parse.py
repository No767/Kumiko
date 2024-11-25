import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

import pytest
from libs.utils import parse_datetime


@pytest.fixture(scope="session", autouse=True)
def load_dict():
    return {"message": "Hello World", "created_at": datetime.now(tz=timezone.utc)}


def test_parse_date_obj():
    date = datetime.now(tz=timezone.utc)
    res = parse_datetime(datetime=date)
    assert isinstance(res, datetime)  # nosec


def test_parse_date_str():
    date = datetime.now(tz=timezone.utc).isoformat()
    res = parse_datetime(datetime=date)
    assert isinstance(res, datetime)  # nosec
