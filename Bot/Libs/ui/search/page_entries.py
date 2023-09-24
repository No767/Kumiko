from yarl import URL

from .structs import AniListAnime, AniListManga, ModrinthProject
from .utils import (
    format_list,
    format_optional_time,
    format_time,
    truncate_excess_anilist_desc,
    truncate_excess_desc,
)


class ModrinthProjectEntry:
    __slots__ = "entry"

    def __init__(self, entry: ModrinthProject):
        self.entry = entry

    def to_dict(self):
        project_url = (
            URL("https://modrinth.com")
            / self.entry.project_type
            / self.entry.project_slug
        )
        desc = f"""
        {truncate_excess_desc(self.entry.description)}
        
        **------**
        
        **Categories**: {', '.join(self.entry.display_categories).rstrip(',')}
        **Client Side:** {self.entry.client_side}
        **Server Side:** {self.entry.server_side}
        **Versions**: {', '.join(self.entry.versions).rstrip(',')}
        **Date Created:** {format_time(self.entry.date_created)}
        **Date Updated:** {format_time(self.entry.date_updated)}
        **URL**: {str(project_url)}
        **License:** {self.entry.license or 'None'}
        """
        data = {
            "title": self.entry.title,
            "description": desc,
            "thumbnail": self.entry.icon_url,
            "fields": [
                {"name": "Author", "value": self.entry.author},
                {"name": "Project Type", "value": self.entry.project_type},
                {"name": "Latest Version", "value": self.entry.latest_version},
            ],
        }
        return data


class AniListMangaEntry:
    __slots__ = "entry"

    def __init__(self, entry: AniListManga):
        self.entry = entry

    def to_dict(self):
        mal_url = URL("https://myanimelist.net/manga") / str(self.entry.mal_id)
        tab = "\t"
        replace_br = (
            self.entry.description.replace("<br>", tab)
            if self.entry.description is not None
            else None
        )
        desc = f"""
        {truncate_excess_anilist_desc(replace_br, self.entry.site_url, 1500)}
        
        **------**
        
        **Native Title**: {self.entry.title.native}
        **English Title**: {self.entry.title.english}
        **Alternate Title**: {format_list(self.entry.synonyms)}
        **Status**: {self.entry.status}
        **Format**: {self.entry.format}
        **Is Adult?**: {self.entry.is_adult}
        **Start Date**: {format_optional_time(self.entry.start_date)}
        **End Date**: {format_optional_time(self.entry.end_date)}
        **Chapters**: {self.entry.chapters or 0} ({self.entry.volumes or 0} volume(s))
        **Site URL**: {self.entry.site_url}
        **MyAnimeList URL**: {mal_url}
        **Genres**: {format_list(self.entry.genres)}
        **Tags**: {format_list(self.entry.tags)}
        **Scores**: 
            | - Average: {self.entry.avg_score} 
            | - Mean: {self.entry.mean_score}
            | - Popularity: {self.entry.popularity}
            | - Trending: {self.entry.trending}
        """
        data = {
            "title": f"{self.entry.title.romaji}",
            "description": desc,
            "image": self.entry.cover_image,
        }
        return data


class AniListAnimeEntry:
    __slots__ = "entry"

    def __init__(self, entry: AniListAnime):
        self.entry = entry

    def to_dict(self):
        mal_url = URL("https://myanimelist.net/manga") / str(self.entry.mal_id)
        tab = "\t"
        replace_br = (
            self.entry.description.replace("<br>", tab)
            if self.entry.description is not None
            else None
        )
        desc = f"""
        {truncate_excess_anilist_desc(replace_br, self.entry.site_url, 1500)}
        
        **------**
        
        **Native Title**: {self.entry.title.native}
        **English Title**: {self.entry.title.english}
        **Alternate Title**: {format_list(self.entry.synonyms)}
        **Status**: {self.entry.status}
        **Format**: {self.entry.format}
        **Is Adult?**: {self.entry.is_adult}
        **Start Date**: {format_optional_time(self.entry.start_date)}
        **End Date**: {format_optional_time(self.entry.end_date)}
        **Episodes**: {self.entry.episodes or 0} ({self.entry.duration or 0} minute(s))
        **Site URL**: {self.entry.site_url}
        **MyAnimeList URL**: {mal_url}
        **Genres**: {format_list(self.entry.genres)}
        **Tags**: {format_list(self.entry.tags)}
        **Scores**: 
            | - Average: {self.entry.avg_score} 
            | - Mean: {self.entry.mean_score}
            | - Popularity: {self.entry.popularity}
            | - Trending: {self.entry.trending}
        """
        data = {
            "title": f"{self.entry.title.romaji}",
            "description": desc,
            "image": self.entry.cover_image,
        }
        return data
