from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

from dateutil.relativedelta import relativedelta

if TYPE_CHECKING:
    from collections.abc import Sequence


class Plural:
    def __init__(self, value: int):
        self.value: int = value

    def __format__(self, format_spec: str) -> str:
        v = self.value
        singular, _, plural = format_spec.partition("|")
        plural = plural or f"{singular}s"
        if abs(v) != 1:
            return f"{v} {plural}"
        return f"{v} {singular}"


def human_join(seq: Sequence[str], delim: str = ", ", final: str = "or") -> str:
    size = len(seq)
    if size == 0:
        return ""

    if size == 1:
        return seq[0]

    if size == 2:
        return f"{seq[0]} {final} {seq[1]}"

    return delim.join(seq[:-1]) + f" {final} {seq[-1]}"


# The old system does work, but as noted, can be inaccurate
# This system is from RDanny and should provide more accurate results
def human_timedelta(
    dt: datetime.datetime,
    *,
    source: Optional[datetime.datetime] = None,
    accuracy: Optional[int] = 3,
    brief: bool = False,
    suffix: bool = True,
) -> str:
    now = source or datetime.datetime.now(datetime.UTC)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.UTC)

    if now.tzinfo is None:
        now = now.replace(tzinfo=datetime.UTC)

    # Microsecond free zone
    now = now.replace(microsecond=0)
    dt = dt.replace(microsecond=0)

    # This implementation uses relativedelta instead of the much more obvious
    # divmod approach with seconds because the seconds approach is not entirely
    # accurate once you go over 1 week in terms of accuracy since you have to
    # hardcode a month as 30 or 31 days.
    # A query like "11 months" can be interpreted as "!1 months and 6 days"
    if dt > now:
        delta = relativedelta(dt, now)
        output_suffix = ""
    else:
        delta = relativedelta(now, dt)
        output_suffix = " ago" if suffix else ""

    attrs = [
        ("year", "y"),
        ("month", "mo"),
        ("day", "d"),
        ("hour", "h"),
        ("minute", "m"),
        ("second", "s"),
    ]

    output = []
    for attr, brief_attr in attrs:
        elem = getattr(delta, attr + "s")
        if not elem:
            continue

        if attr == "day":
            weeks = delta.weeks
            if weeks:
                elem -= weeks * 7
                if not brief:
                    output.append(format(Plural(weeks), "week"))
                else:
                    output.append(f"{weeks}w")

        if elem <= 0:
            continue

        if brief:
            output.append(f"{elem}{brief_attr}")
        else:
            output.append(format(Plural(elem), attr))

    if accuracy is not None:
        output = output[:accuracy]

    if len(output) == 0:
        return "now"
    if not brief:
        return human_join(output, final="and") + output_suffix
    return " ".join(output) + output_suffix


def format_dt(dt: datetime.datetime, style: Optional[str] = None) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.UTC)

    if style is None:
        return f"<t:{int(dt.timestamp())}>"
    return f"<t:{int(dt.timestamp())}:{style}>"
