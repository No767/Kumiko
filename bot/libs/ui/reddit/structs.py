import msgspec


class RedditEntry(msgspec.Struct):
    title: str
    description: str
    image_url: str
    author: str
    upvotes: int
    nsfw: bool
    flair: str
    num_of_comments: int
    post_permalink: str
    created_utc: int


class RedditMemeEntry(msgspec.Struct):
    title: str
    url: str
    author: str
    subreddit: str
    ups: int
    nsfw: bool
    spoiler: bool
    reddit_url: str
