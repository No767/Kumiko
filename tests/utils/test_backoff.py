import os
import sys
from pathlib import Path

import pytest

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "Bot", "Libs")
sys.path.append(packagePath)

from kumiko_utils import backoff


@pytest.fixture(scope="session")
def backoff_values():
    return (5, 0)


def test_backoff(backoff_values):
    backoff_sec, backoff_sec_index = backoff_values
    sleepAmt = backoff(backoff_sec, backoff_sec_index)
    assert sleepAmt <= 6.0 and sleepAmt >= 5.0  # nosec


def test_backoff_loop(backoff_values):
    backoff_sec, backoff_sec_index = backoff_values
    backoffTime = 0
    for _ in range(5):
        backoffTime = backoff(backoff_sec, backoff_sec_index)
        backoff_sec_index += 1

    assert backoffTime == 60.0  # nosec
