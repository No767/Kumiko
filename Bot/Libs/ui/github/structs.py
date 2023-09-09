import datetime
from typing import List, Union

import msgspec


class GitHubIssueLabel(msgspec.Struct):
    name: str
    description: str


class GitHubUser(msgspec.Struct):
    name: str
    avatar_url: str
    url: str


class GitHubIssue(msgspec.Struct):
    title: str
    body: str
    state: str
    state_reason: Union[str, None]
    url: str
    labels: List[GitHubIssueLabel]
    user: GitHubUser
    assignees: List[GitHubUser]
    closed_at: Union[datetime.datetime, None]
    created_at: Union[datetime.datetime, None]
    updated_at: Union[datetime.datetime, None]


class GitHubCommentReactions(msgspec.Struct):
    total_count: int
    plus_1: int
    minus_1: int
    laugh: int
    hooray: int
    confused: int
    heart: int
    rocket: int
    eyes: int


class GitHubIssueComment(msgspec.Struct):
    body: str
    url: str
    author: GitHubUser
    created_at: datetime.datetime
    updated_at: datetime.datetime
    reactions: GitHubCommentReactions
