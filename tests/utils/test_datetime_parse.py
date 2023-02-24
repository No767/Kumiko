import os
import sys
from datetime import datetime, timezone
from pathlib import Path

path = Path(__file__).parents[2]
packagePath = os.path.join(str(path), "Bot", "Libs")
sys.path.append(packagePath)

from kumiko_utils import parseDatetime


def test_parse_date_obj():
    currDate = datetime.now(tz=timezone.utc)
    res = parseDatetime(datetime=currDate)
    assert isinstance(res, datetime)  # nosec


def test_parse_date_str():
    currDate = datetime.now(tz=timezone.utc).isoformat()
    res = parseDatetime(datetime=currDate)
    assert isinstance(res, datetime)  # nosec
