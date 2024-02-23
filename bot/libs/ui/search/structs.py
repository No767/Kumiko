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


class AniListMediaTitle(msgspec.Struct):
    native: str
    english: str
    romaji: str


class AniListManga(msgspec.Struct):
    title: AniListMediaTitle
    status: str
    description: str
    format: str
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    chapters: int
    volumes: int
    cover_image: str
    cover_image_color: str
    genres: List[str]
    tags: List[str]
    synonyms: List[str]
    mal_id: int
    site_url: str
    avg_score: int
    mean_score: int
    popularity: int
    trending: int
    is_adult: bool


class AniListAnime(msgspec.Struct):
    title: AniListMediaTitle
    status: str
    description: str
    format: str
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    episodes: int
    duration: int
    cover_image: str
    cover_image_color: str
    genres: List[str]
    tags: List[str]
    synonyms: List[str]
    mal_id: int
    site_url: str
    avg_score: int
    mean_score: int
    popularity: int
    trending: int
    is_adult: bool
