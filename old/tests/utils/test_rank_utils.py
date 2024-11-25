import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from libs.utils import calc_petals, calc_rank


def test_calc_rank():
    predicted_rank = calc_rank(100)
    assert predicted_rank == 1


def test_calc_petals():
    predicted_petals = calc_petals(1)
    assert predicted_petals == 579
