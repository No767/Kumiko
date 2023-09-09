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


class GitHubLicense(msgspec.Struct):
    name: str
    spdx_id: str


class GitHubRepo(msgspec.Struct):
    name: str
    full_name: str
    private: bool
    owner: GitHubUser
    url: str
    description: str
    fork: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    pushed_at: datetime.datetime
    homepage: Union[str, None]
    git_url: str
    ssh_url: str
    clone_url: str
    star_count: int
    watchers: int
    language: str
    forks: int
    archived: bool
    open_issues: int
    license: Union[GitHubLicense, None]
    topics: List[str]


class GitHubReleaseAsset(msgspec.Struct):
    name: str
    label: str
    state: str
    size: int
    download_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    download_url: str


class GitHubRepoReleases(msgspec.Struct):
    url: str
    author: GitHubUser
    tag_name: str
    name: str
    prerelease: bool
    assets: List[GitHubReleaseAsset]
    created_at: datetime.datetime
    published_at: datetime.datetime
    tarball_url: str
    zipball_url: str
    body: str


class GitHubParentCommit(msgspec.Struct):
    sha: str
    url: str


class GitHubCommit(msgspec.Struct):
    author: GitHubUser
    commit_date: datetime.datetime
    message: str
    url: str
    parents: List[GitHubParentCommit]
