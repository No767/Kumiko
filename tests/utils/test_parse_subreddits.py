import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.utils import parse_subreddit


def test_rslash_egg_irl():
    assert parse_subreddit("r/egg_irl") == "egg_irl"


def test_egg_irl():
    assert parse_subreddit("egg_irl") == "egg_irl"


def test_none_subreddit():
    assert parse_subreddit(subreddit=None) == "all"
