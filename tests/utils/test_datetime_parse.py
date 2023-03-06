import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

import pytest
from Libs.utils import encodeDatetime, parseDatetime


@pytest.fixture(scope="session", autouse=True)
def load_dict():
    return {"message": "Hello World", "created_at": datetime.now(tz=timezone.utc)}


def test_parse_date_obj():
    currDate = datetime.now(tz=timezone.utc)
    res = parseDatetime(datetime=currDate)
    assert isinstance(res, datetime)  # nosec


def test_parse_date_str():
    currDate = datetime.now(tz=timezone.utc).isoformat()
    res = parseDatetime(datetime=currDate)
    assert isinstance(res, datetime)  # nosec


def test_encode_datetime(load_dict):
    assert isinstance(encodeDatetime(dict=load_dict)["created_at"], str)  # nosec
