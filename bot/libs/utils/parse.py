from __future__ import annotations

import re
from datetime import datetime
from typing import Optional, Union

import ciso8601
import dateparser


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


def parse_subreddit(subreddit: Union[str, None]) -> str:
    """Parses a subreddit name to be used in a reddit url

    Args:
        subreddit (Union[str, None]): Subreddit name to parse

    Returns:
        str: Parsed subreddit name
    """
    if subreddit is None:
        return "all"
    return re.sub(r"^[r/]{2}", "", subreddit, re.IGNORECASE)


def parse_dt(dt: str) -> Optional[datetime]:
    """Parses an string representation of datetime (e.g. Jan 1)
    into an `datetime.datetime` instance

    Args:
        dt (str): String representation of datetime

    Returns:
        Optional[datetime]: `datetime.datetime` instance
    """
    return dateparser.parse(dt)
