import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.utils import format_greedy


def test_format_greedy_3plus():
    assert (format_greedy(["a", "b", "c"]) == "a, b, and c") and (
        format_greedy(["a", "b", "c", "d"]) == "a, b, c, and d"
    )


def test_format_greedy_2():
    assert format_greedy(["a", "b"]) == "a and b"


def test_format_greedy_1():
    assert format_greedy(["a"]) == "a"


def test_format_greedy_empty():
    assert format_greedy([]) == ""
