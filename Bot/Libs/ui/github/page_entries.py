from .structs import GitHubIssueComment, GitHubUser
from .utils import parse_optional_datetimes


class GitHubUserPageEntry:
    def __init__(self, entry: GitHubUser):
        self.entry = entry

    def to_dict(self):
        data = {
            "title": self.entry.name,
            "description": f"**Profile URL**: {self.entry.url}",
            "thumbnail": self.entry.avatar_url,
        }
        return data


class GitHubIssuesCommentsPageEntry:
    def __init__(self, entry: GitHubIssueComment):
        self.entry = entry

    def to_dict(self):
        data = {
            "title": f"Comment by {self.entry.author.name}",
            "description": self.entry.body or None,
            "fields": [
                {
                    "name": "Created At",
                    "value": parse_optional_datetimes(self.entry.created_at),
                },
                {"name": "URL", "value": self.entry.url},
            ],
            "thumbnail": self.entry.author.avatar_url,
        }
        return data
