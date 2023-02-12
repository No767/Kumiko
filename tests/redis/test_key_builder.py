import os
import sys
from pathlib import Path

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "Bot", "Libs")
sys.path.append(packagePath)

from kumiko_cache import commandKeyBuilder, defaultKeyBuilder


def test_default_key_builder():
    assert isinstance(defaultKeyBuilder(), str)  # nosec


def test_commmand_key_builder():
    assert (  # nosec
        isinstance(commandKeyBuilder(), str)
        and commandKeyBuilder(
            prefix="cache", namespace="kumiko", id=123, command="test"
        )
        == "cache:kumiko:123:test"
    )
