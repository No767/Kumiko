import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

import builtins

from Libs.cache import MemoryCache, setupMemCacheBuiltin


def test_mem_cache_builtin():
    setupMemCacheBuiltin()
    assert isinstance(builtins.memCache, MemoryCache)  # nosec
