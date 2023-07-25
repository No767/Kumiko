import re
import ssl
from datetime import datetime, timedelta
from typing import Any, Dict, Union

import ciso8601

# From https://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
# Answer: https://stackoverflow.com/a/51916936
# datetimeParseRegex = re.compile(r'^((?P<days>[\.\d]+?)d)?((?P<hours>[\.\d]+?)h)?((?P<minutes>[\.\d]+?)m)?((?P<seconds>[\.\d]+?)s)?$')
datetimeParseRegex = re.compile(
    r"^((?P<weeks>[\.\d]+?)w)? *"
    r"^((?P<days>[\.\d]+?)d)? *"
    r"((?P<hours>[\.\d]+?)h)? *"
    r"((?P<minutes>[\.\d]+?)m)? *"
    r"((?P<seconds>[\.\d]+?)s?)?$"
)


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


def parseSubreddit(subreddit: Union[str, None]) -> str:
    """Parses a subreddit name to be used in a reddit url

    Args:
        subreddit (Union[str, None]): Subreddit name to parse

    Returns:
        str: Parsed subreddit name
    """
    if subreddit is None:
        return "all"
    return re.sub(r"^[r/]{2}", "", subreddit, re.IGNORECASE)


def parseTimeStr(time_str: str) -> Union[timedelta, None]:
    """Parse a time string e.g. (2h13m) into a timedelta object.

    Taken straight from https://stackoverflow.com/a/4628148

    Args:
        time_str (str): A string identifying a duration.  (eg. 2h13m)

    Returns:
        datetime.timedelta: A datetime.timedelta object
    """
    parts = datetimeParseRegex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


def setup_ssl() -> ssl.SSLContext:
    sslctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    sslctx.check_hostname = False
    sslctx.verify_mode = ssl.CERT_NONE
    return sslctx
