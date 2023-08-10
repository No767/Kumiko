from datetime import datetime

from discord.utils import format_dt

from .structs import RedditEntry, RedditMemeEntry


class RedditPageEntry:
    def __init__(self, entry: RedditEntry):
        self.entry = entry

    def to_dict(self):
        data = {
            "title": self.entry.title,
            "description": self.entry.description,
            "image": self.entry.image_url,
            "fields": [
                {"name": "Author", "value": self.entry.author},
                {"name": "Upvotes", "value": self.entry.upvotes},
                {"name": "NSFW", "value": self.entry.nsfw},
                {"name": "Flair", "value": self.entry.flair},
                {"name": "Number of Comments", "value": self.entry.num_of_comments},
                {
                    "name": "Reddit URL",
                    "value": f"https://reddit.com{self.entry.post_permalink}",
                },
                {
                    "name": "Created At",
                    "value": format_dt(datetime.fromtimestamp(self.entry.created_utc)),
                },
            ],
        }
        return data


class RedditMemePageEntry:
    def __init__(self, entries: RedditMemeEntry):
        self.entry = entries

    def to_dict(self):
        data = {
            "title": self.entry.title,
            "image": self.entry.url,
            "fields": [
                {"name": "Author", "value": self.entry.author},
                {"name": "Subreddit", "value": self.entry.subreddit},
                {"name": "Upvotes", "value": self.entry.ups},
                {"name": "NSFW", "value": self.entry.nsfw},
                {"name": "Spoiler", "value": self.entry.spoiler},
                {"name": "Reddit URL", "value": self.entry.reddit_url},
            ],
        }
        return data
