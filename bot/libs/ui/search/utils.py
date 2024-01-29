import datetime
from typing import List, Optional

from discord.utils import format_dt


def truncate_excess_desc(string: str, amount: int = 2000) -> str:
    if len(string) > amount:
        return string[: amount - 3] + "..."
    return string


def truncate_excess_anilist_desc(
    string: Optional[str], site_url: str, amount: int = 2000
) -> Optional[str]:
    if string is not None and len(string) > amount:
        return string[: amount - 60] + f"...\n[Read more on AniList]({site_url})"
    return string or None


def format_time(dt: datetime.datetime):
    offset = format_dt(dt.astimezone(datetime.timezone.utc), "R")
    fmt_time = format_dt(dt.astimezone(datetime.timezone.utc))
    return f"{fmt_time} ({offset})"


def format_optional_time(dt: Optional[datetime.datetime]) -> str:
    if dt is None:
        return "None"
    offset = format_dt(dt.astimezone(datetime.timezone.utc), "R")
    fmt_time = format_dt(dt.astimezone(datetime.timezone.utc))
    return f"{fmt_time} ({offset})"


def format_list(items: List[str]) -> str:
    return ", ".join(items).rstrip(",")
