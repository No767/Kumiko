import os
import re
import ssl
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

import ciso8601
import dateparser
from discord.utils import utcnow
from dotenv import dotenv_values

from .embeds import ErrorEmbed


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


def setup_ssl(
    ca_path: Union[str, None],
    cert_path: str,
    key_path: Union[str, None],
    key_password: Union[str, None],
) -> ssl.SSLContext:
    sslctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_path)
    sslctx.check_hostname = True
    sslctx.load_cert_chain(cert_path, key_path, key_password)
    return sslctx


def is_docker() -> bool:
    path = "/proc/self/cgroup"
    return os.path.exists("/.dockerenv") or (
        os.path.isfile(path) and any("docker" in line for line in open(path))
    )


def read_env(path: Path, read_from_file: bool = True) -> Dict[str, Optional[str]]:
    if is_docker() or read_from_file is False:
        return {**os.environ}
    return {**dotenv_values(path)}


def parse_dt(dt: str) -> Optional[datetime]:
    return dateparser.parse(dt)


def make_error_embed(error: Exception) -> ErrorEmbed:
    error_traceback = "\n".join(traceback.format_exception_only(type(error), error))
    embed = ErrorEmbed()
    desc = f"""
    Uh oh! It seems like there was an issue. For support, please visit [Kumiko's Support Server](https://discord.gg/ns3e74frqn) to get help!
    
    **Error**:
    ```{error_traceback}```
    """
    embed.description = "\n".join(desc)
    embed.set_footer(text="Happened At")
    embed.timestamp = utcnow()
    return embed
