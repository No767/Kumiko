import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.cache import CommandKeyBuilder


def test_commmand_key_builder():
    assert (  # nosec
        isinstance(CommandKeyBuilder(), str)
        and CommandKeyBuilder(
            prefix="cache", namespace="kumiko", id=123, command="test"
        )
        == "cache:kumiko:123:test"
    )
