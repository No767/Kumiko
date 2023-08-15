import sys
from pathlib import Path

from dotenv import load_dotenv

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

load_dotenv()

from Libs.cog_utils.pronouns import *


def test_pronoun():
    pronouns = ["she", "they", "it"]
    res = parse_pronouns(pronouns)
    assert res == "she/her, they/them, it/its"
