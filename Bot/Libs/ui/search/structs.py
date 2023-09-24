import datetime
from typing import List, Optional

import msgspec


class ModrinthProject(msgspec.Struct):
    title: str
    description: str
    display_categories: List[str]
    client_side: str
    server_side: str
    project_type: str
    project_slug: str
    downloads: int
    icon_url: str
    author: str
    versions: List[str]
    latest_version: str
    license: Optional[str]
    date_created: datetime.datetime
    date_updated: datetime.datetime
