import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache.serializers import MsgPackSerializer


@pytest.fixture(autouse=True, scope="session")
def load_data():
    return "Hello"


def test_msgpack_dumps(load_data):
    s = MsgPackSerializer()
    assert isinstance(s.dumps(value=load_data), bytes)  # nosec


def test_msgpack_loads(load_data):
    s = MsgPackSerializer()
    assert isinstance(s.loads(value=s.dumps(value=load_data)), str)  # nosec


def test_msgpack_loads_none():
    s = MsgPackSerializer()
    assert s.loads(value=None) is None  # nosec
