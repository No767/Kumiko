import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from libs.cache import command_key_builder


def test_commmand_key_builder():
    assert (  # nosec
        isinstance(command_key_builder(), str)
        and command_key_builder(
            prefix="cache", namespace="kumiko", id=123, command="test"
        )
        == "cache:kumiko:123:test"
    )
