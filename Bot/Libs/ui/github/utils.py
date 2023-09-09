import datetime
from typing import Union

from discord.utils import format_dt
from Libs.utils import parse_datetime


def parse_state(state: str):
    state_data = {
        "open": "<:status_online:596576749790429200>",
        "completed": "<:greenTick:596576670815879169>",
        "closed": "<:status_dnd:596576774364856321>",
    }
    return state_data[state]


def parse_optional_datetimes(dt: Union[datetime.datetime, None]) -> str:
    if dt is None:
        return "N/A"
    return format_dt(parse_datetime(dt))


def truncate_excess_string(string: str) -> str:
    if len(string) > 4096:
        return string[:4093] + "..."
    return string
