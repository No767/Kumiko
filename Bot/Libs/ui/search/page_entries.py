from yarl import URL

from .structs import ModrinthProject
from .utils import format_time, truncate_excess_desc


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
