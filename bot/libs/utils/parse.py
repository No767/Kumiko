from __future__ import annotations

from datetime import datetime
from typing import Union

import ciso8601


def parse_datetime(datetime: Union[datetime, str]) -> datetime:
    """Parses a datetime object or a string into a datetime object

    Args:
        datetime (Union[datetime.datetime, str]): Datetime object or string to parse

    Returns:
        datetime.datetime: Parsed datetime object
    """
    if isinstance(datetime, str):
        return ciso8601.parse_datetime(datetime)
    return datetime
