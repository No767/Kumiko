from datetime import datetime
from typing import Any, Dict, Union

import ciso8601


def parseDatetime(datetime: Union[datetime, str]) -> datetime:
    """Parses a datetime object or a string into a datetime object

    Args:
        datetime (Union[datetime.datetime, str]): Datetime object or string to parse

    Returns:
        datetime.datetime: Parsed datetime object
    """
    if isinstance(datetime, str):
        return ciso8601.parse_datetime(datetime)
    return datetime


def encodeDatetime(dict: Dict[str, Any]) -> Dict[str, Any]:
    """Takes a dictionary and encodes all datetime objects into ISO 8601 strings

    Args:
        dict (Dict[str, Any]): Dictionary to encode

    Returns:
        Dict[str, Any]: The dictionary with all datetime objects encoded as ISO 8601 strings
    """
    for k, v in dict.items():
        if isinstance(v, datetime):
            dict[k] = v.isoformat()
    return dict
