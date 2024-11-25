from discord.utils import format_dt

from .structs import (
    GitHubCommit,
    GitHubIssueComment,
    GitHubRepoReleases,
    GitHubUser,
)
from .utils import parse_optional_datetimes, truncate_excess_string


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


class GitHubReleasePageEntry:
    def __init__(self, entry: GitHubRepoReleases):
        self.entry = entry

    def to_dict(self):
        data = {
            "title": self.entry.name,
            "description": truncate_excess_string(self.entry.body),
            "fields": [
                {"name": "Prerelease?", "value": self.entry.prerelease},
                {"name": "Created At", "value": format_dt(self.entry.created_at)},
                {
                    "name": "Source Download URL",
                    "value": f"{self.entry.tarball_url}, {self.entry.zipball_url}",
                },
                {
                    "name": "Assets Download URL",
                    "value": ",".join(
                        [asset.download_url for asset in self.entry.assets]
                    ).rstrip(","),
                },
            ],
        }
        return data


class GitHubCommitPageEntry:
    def __init__(self, entry: GitHubCommit):
        self.entry = entry

    def to_dict(self):
        data = {
            "title": self.entry.author.name,
            "description": truncate_excess_string(self.entry.message) or "None",
            "fields": [
                {"name": "Committed at", "value": format_dt(self.entry.commit_date)},
                {
                    "name": "Parent Commits",
                    "value": ", ".join(
                        [commit.sha for commit in self.entry.parents]
                    ).rstrip(","),
                },
                {"name": "URL", "value": self.entry.url},
            ],
            "thumbnail": self.entry.author.avatar_url,
        }
        return data
