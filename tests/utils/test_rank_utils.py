import sys
from pathlib import Path

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

from Libs.utils import calc_petals, calc_rank


def test_calc_rank():
    predictedRank = calc_rank(100)
    assert predictedRank == 1


def test_calc_petals():
    predictedPetals = calc_petals(1)
    assert predictedPetals == 579
