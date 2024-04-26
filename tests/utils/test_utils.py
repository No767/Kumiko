import datetime
import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from libs.utils import is_docker, parse_datetime, parse_dt, produce_error_embed


def test_is_docker():
    if is_docker() is False:
        assert is_docker() is False
        return
    assert is_docker() is True


def test_parse_dt():
    input_str = "tomorrow"
    dt = parse_dt(input_str)
    assert isinstance(dt, datetime.datetime)

    input_str = "fsoudfsbfdubfsudfsufbosudfsbofudoffdf"
    dt = parse_dt(input_str)
    assert dt is None


def test_produce_error_embed():
    with pytest.raises(KeyError) as e:
        raise KeyError("Failed Embed")

    error_embed = produce_error_embed(e.value)
    error_dict = error_embed.to_dict()
    title = error_dict["title"]  # type: ignore
    desc = error_dict["description"]  # type: ignore
    timestamp = error_dict["timestamp"]  # type: ignore
    assert (
        title == "Oh no, an error has occurred!"
        and isinstance(desc, str)
        and isinstance(parse_datetime(timestamp), datetime.datetime)
    )
