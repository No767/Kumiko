import datetime
from typing import Dict, Optional

from dateutil.parser import parse


def parse_anilist_dates(date: Dict[str, str]) -> Optional[datetime.datetime]:
    if None in date.values():
        return None
    formatted_date = f"{date['month']}-{date['day']}-{date['year']}"
    return parse(formatted_date)
