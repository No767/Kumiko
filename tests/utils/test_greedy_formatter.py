import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.utils import formatGreedy


def test_format_greedy_3plus():
    assert (formatGreedy(["a", "b", "c"]) == "a, b, and c") and (
        formatGreedy(["a", "b", "c", "d"]) == "a, b, c, and d"
    )


def test_format_greedy_2():
    assert formatGreedy(["a", "b"]) == "a and b"


def test_format_greedy_1():
    assert formatGreedy(["a"]) == "a"


def test_format_greedy_empty():
    assert formatGreedy([]) == ""
