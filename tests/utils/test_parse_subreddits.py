import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.utils import parseSubreddit


def test_rslash_egg_irl():
    assert parseSubreddit("r/egg_irl") == "egg_irl"


def test_egg_irl():
    assert parseSubreddit("egg_irl") == "egg_irl"


def test_none_subreddit():
    assert parseSubreddit(subreddit=None) == "all"
