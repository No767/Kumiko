from __future__ import annotations

import os
import re
import traceback
from datetime import datetime
from typing import List, Union

import ciso8601
import discord

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


def is_docker() -> bool:
    """Checks if the current environment is running in Docker

    Returns:
        bool: Returns `True` if in fact it is an Docker environment,
        `False` if not
    """
    path = "/proc/self/cgroup"
    return os.path.exists("/.dockerenv") or (
        os.path.isfile(path) and any("docker" in line for line in open(path))
    )


def format_greedy(list: List[str]) -> str:
    """Formats a Greedy list into a human-readable string

    For example, if we had a list of ["a", "b", "c"], it would return "a, b, and c".
    If we had a list of ["a", "b"], it would return "a and b".
    If we had a list of ["a"], it would return "a".
    If we had a list of [], it would return "".

    Args:
        list: The list of strings to format

    Returns:
        str: The formatted string
    """
    if len(list) >= 3:
        return f"{', '.join(list[:-1])}, and {list[-1]}"
    elif len(list) == 2:
        return " and ".join(list)
    return "".join(list)


def produce_error_embed(error: Exception) -> ErrorEmbed:
    """Produces a standard error embed

    Args:
        error (Exception): The error

    Returns:
        ErrorEmbed: An `ErrorEmbed` instance with the standard preset
    """
    error_traceback = "\n".join(traceback.format_exception_only(type(error), error))
    embed = ErrorEmbed()
    desc = f"""
    Uh oh! It seems like there was an issue. For support, please visit [Kumiko's Support Server](https://discord.gg/ns3e74frqn) to get help!
    
    **Error**:
    ```{error_traceback}```
    """
    embed.description = desc
    embed.set_footer(text="Happened At")
    embed.timestamp = discord.utils.utcnow()
    return embed
