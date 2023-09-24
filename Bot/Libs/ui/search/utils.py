import datetime

from discord.utils import format_dt


def truncate_excess_desc(string: str, amount: int = 2000) -> str:
    if len(string) > amount:
        return string[: amount - 3] + "..."
    return string


def format_time(dt: datetime.datetime):
    offset = format_dt(dt.astimezone(datetime.timezone.utc), "R")
    fmt_time = format_dt(dt.astimezone(datetime.timezone.utc))
    return f"{fmt_time} ({offset})"
