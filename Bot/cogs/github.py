import ciso8601
import orjson
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.ui.github import (
    GitHubCommentReactions,
    GitHubCommit,
    GitHubCommitPages,
    GitHubIssue,
    GitHubIssueComment,
    GitHubIssueLabel,
    GithubIssuesPages,
    GitHubLicense,
    GitHubParentCommit,
    GitHubReleaseAsset,
    GitHubRepo,
    GithubRepoPages,
    GitHubRepoReleases,
    GitHubUser,
)
from yarl import URL


class Github(commands.Cog):
    """Search for releases and repos on GitHub"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session
        self.gh_key = self.bot.config["apis"]["github"]
        self.base_url = URL("https://api.github.com/repos/")
        self.headers = {
            "Authorization": f"Bearer: {self.gh_key}",
            "accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<:githubmarkwhite:1127906278509912185>")

    @commands.hybrid_group(name="github")
    async def github(self, ctx: commands.Context) -> None:
        """Github search and utility commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @github.command(name="issues")
    @app_commands.describe(
        owner="The owner or org of the repo",
        repo="The repo name",
        issue="The issue number",
    )
    async def issues(
        self, ctx: commands.Context, owner: str, repo: str, issue: int
    ) -> None:
        """Obtains detailed information about the given issue"""
        issues_url = self.base_url / str(issue)
        comments_url = self.base_url / str(issue) / "comments"
        async with self.session.get(
            issues_url, headers=self.headers
        ) as issues_res, self.session.get(
            comments_url, headers=self.headers
        ) as comments_res:
            issue_data = await issues_res.json(loads=orjson.loads)
            comments_data = await comments_res.json(loads=orjson.loads)

            if issues_res.status == 404 or comments_res.status == 404:
                await ctx.send("Could not find either the issue or the repo itself")
                return

            issue_entry = GitHubIssue(
                title=issue_data["title"],
                body=issue_data["body"],
                state=issue_data["state"],
                state_reason=issue_data["state_reason"],
                url=issue_data["html_url"],
                labels=[
                    GitHubIssueLabel(
                        name=label["name"], description=label["description"]
                    )
                    for label in issue_data["labels"]
                ],
                user=GitHubUser(
                    name=issue_data["user"]["login"],
                    avatar_url=issue_data["user"]["avatar_url"],
                    url=issue_data["user"]["html_url"],
                ),
                assignees=[
                    GitHubUser(
                        name=assignee["login"],
                        avatar_url=assignee["avatar_url"],
                        url=assignee["html_url"],
                    )
                    for assignee in issue_data["assignees"]
                ],
                closed_at=ciso8601.parse_datetime(issue_data["closed_at"]) or None,
                created_at=ciso8601.parse_datetime(issue_data["created_at"]) or None,
                updated_at=ciso8601.parse_datetime(issue_data["updated_at"]) or None,
            )

            converted_comments = [
                GitHubIssueComment(
                    body=comment["body"],
                    url=comment["html_url"],
                    author=GitHubUser(
                        name=comment["user"]["login"],
                        avatar_url=comment["user"]["avatar_url"],
                        url=comment["user"]["html_url"],
                    ),
                    created_at=ciso8601.parse_datetime(comment["created_at"]),
                    updated_at=ciso8601.parse_datetime(comment["updated_at"]),
                    reactions=GitHubCommentReactions(
                        total_count=comment["reactions"]["total_count"],
                        plus_1=comment["reactions"]["+1"],
                        minus_1=comment["reactions"]["-1"],
                        laugh=comment["reactions"]["laugh"],
                        hooray=comment["reactions"]["hooray"],
                        confused=comment["reactions"]["confused"],
                        heart=comment["reactions"]["heart"],
                        rocket=comment["reactions"]["rocket"],
                        eyes=comment["reactions"]["eyes"],
                    ),
                )
                for comment in comments_data
            ]

            pages = GithubIssuesPages(
                issue_entry=issue_entry, comments_entries=converted_comments, ctx=ctx
            )
            await pages.start()

    @github.command(name="repo")
    @app_commands.describe(
        owner="The owner of the repo (eg. No767)", repo="The repo name (eg. Kumiko)"
    )
    async def repo(self, ctx: commands.Context, owner: str, repo: str) -> None:
        """Provides detailed information about the given repo"""
        repo_url = self.base_url / owner / repo
        releases_url = self.base_url / owner / repo / "releases"
        async with self.session.get(
            repo_url, headers=self.headers
        ) as repo_res, self.session.get(
            releases_url, headers=self.headers
        ) as releases_res:
            repo_data = await repo_res.json(loads=orjson.loads)
            releases_data = await releases_res.json(loads=orjson.loads)

            if repo_res.status == 404 or releases_res.status == 404:
                await ctx.send("Could not find either the release or the repo itself")
                return

            repo_entry = GitHubRepo(
                name=repo_data["name"],
                full_name=repo_data["full_name"],
                private=repo_data["private"],
                owner=GitHubUser(
                    name=repo_data["owner"]["login"],
                    avatar_url=repo_data["owner"]["avatar_url"],
                    url=repo_data["owner"]["html_url"],
                ),
                url=repo_data["html_url"],
                description=repo_data["description"],
                fork=repo_data["fork"],
                created_at=ciso8601.parse_datetime(repo_data["created_at"]),
                updated_at=ciso8601.parse_datetime(repo_data["updated_at"]),
                pushed_at=ciso8601.parse_datetime(repo_data["pushed_at"]),
                homepage=repo_data["homepage"],
                git_url=repo_data["git_url"],
                ssh_url=repo_data["ssh_url"],
                clone_url=repo_data["clone_url"],
                star_count=repo_data["stargazers_count"],
                watchers=repo_data["watchers"],
                language=repo_data["language"],
                forks=repo_data["forks"],
                archived=repo_data["archived"],
                open_issues=repo_data["open_issues_count"],
                license=GitHubLicense(
                    name=repo_data["license"]["name"] or "None",
                    spdx_id=repo_data["license"]["spdx_id"] or "None",
                ),
                topics=repo_data["topics"],
            )

            releases_entries = [
                GitHubRepoReleases(
                    url=release["html_url"],
                    author=GitHubUser(
                        name=release["author"]["login"],
                        avatar_url=release["author"]["avatar_url"],
                        url=release["author"]["html_url"],
                    ),
                    tag_name=release["tag_name"],
                    name=release["name"],
                    prerelease=release["prerelease"],
                    assets=[
                        GitHubReleaseAsset(
                            name=asset["name"],
                            label=asset["label"],
                            state=asset["state"],
                            size=asset["size"],
                            download_count=asset["download_count"],
                            created_at=ciso8601.parse_datetime(asset["created_at"]),
                            updated_at=ciso8601.parse_datetime(asset["updated_at"]),
                            download_url=asset["browser_download_url"],
                        )
                        for asset in release["assets"]
                    ],
                    created_at=ciso8601.parse_datetime(release["created_at"]),
                    published_at=ciso8601.parse_datetime(release["published_at"]),
                    tarball_url=release["tarball_url"],
                    zipball_url=release["zipball_url"],
                    body=release["body"],
                )
                for release in releases_data
            ]

            pages = GithubRepoPages(repo_entry, releases_entries, ctx=ctx)
            await pages.start()

    @github.command(name="commits")
    @app_commands.describe(
        owner="The owner of the repo (eg. No767)", repo="The repo name (eg. Kumiko)"
    )
    async def commits(self, ctx: commands.Context, owner: str, repo: str) -> None:
        """Get all of the latest commits from a given repo"""
        params = {"per_page": 75}
        url = self.base_url / owner / repo / "commits"
        async with self.session.get(url, headers=self.headers, params=params) as r:
            data = await r.json(loads=orjson.loads)

            if r.status == 404:
                await ctx.send("Could not find the repo itself")
                return

            converted = [
                GitHubCommit(
                    author=GitHubUser(
                        name=commit["author"]["login"],
                        avatar_url=commit["author"]["avatar_url"],
                        url=commit["author"]["html_url"],
                    ),
                    commit_date=ciso8601.parse_datetime(
                        commit["commit"]["author"]["date"]
                    ),
                    message=commit["commit"]["message"],
                    url=commit["html_url"],
                    parents=[
                        GitHubParentCommit(sha=parent["sha"], url=parent["html_url"])
                        for parent in commit["parents"]
                    ],
                )
                for commit in data
            ]
            pages = GitHubCommitPages(entries=converted, ctx=ctx)
            await pages.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Github(bot))
