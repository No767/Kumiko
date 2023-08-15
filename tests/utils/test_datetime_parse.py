import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

import pytest
from Libs.utils import encode_datetime, parse_datetime, parse_time_str


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


def test_encode_datetime(load_dict):
    assert isinstance(encode_datetime(load_dict)["created_at"], str)  # nosec


def test_parse_time_str():
    assert isinstance(parse_time_str("2h"), timedelta)


def test_parse_time_str_empty():
    assert isinstance(parse_time_str(""), timedelta)  # this should not work...


def test_parse_time_str_invalid():
    assert parse_time_str("what mate") is None
