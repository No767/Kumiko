import os

import ciso8601
import orjson
from discord import PartialEmoji, app_commands
from discord.ext import commands
from discord.utils import format_dt
from dotenv import load_dotenv
from kumikocore import KumikoCore
from Libs.ui.github import (
    GitHubCommentReactions,
    GitHubIssue,
    GitHubIssueComment,
    GitHubIssueLabel,
    GithubIssuesPages,
    GitHubUser,
)
from Libs.utils import Embed
from Libs.utils.pages import EmbedListSource, KumikoPages
from yarl import URL

load_dotenv()

GITHUB_API_KEY = os.environ["GITHUB_API_KEY"]


class Github(commands.Cog):
    """Search for releases and repos on GitHub"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.session = self.bot.session
        self.gh_key = self.bot.config["GITHUB_API_KEY"]

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

        headers = {
            "Authorization": f"Bearer: {GITHUB_API_KEY}",
            "accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        base_url = URL("https://api.github.com/repos/") / owner / repo / "issues"
        issues_url = base_url / str(issue)
        comments_url = base_url / str(issue) / "comments"
        async with self.session.get(
            issues_url, headers=headers
        ) as issues_res, self.session.get(comments_url) as comments_res:
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

    # Force defaults to use Kumiko's repo ?
    @github.command(name="release-list")
    @app_commands.describe(owner="The owner of the repo", repo="The repo to search")
    async def releases(self, ctx: commands.Context, owner: str, repo: str) -> None:
        """Get up to 25 releases for a repo"""
        headers = {
            "Authorization": f"token {GITHUB_API_KEY}",
            "accept": "application/vnd.github+json",
        }
        params = {"per_page": 25}
        async with self.session.get(
            f"https://api.github.com/repos/{owner}/{repo}/releases",
            headers=headers,
            params=params,
        ) as r:
            data = await r.json(loads=orjson.loads)
            if r.status == 404:
                await ctx.send("The release(s) were not found")
                return
            else:
                main_data = [
                    {
                        "title": item["name"],
                        "description": item["body"],
                        "thumbnail": item["author"]["avatar_url"],
                        "fields": [
                            {"name": "Author", "value": item["author"]["login"]},
                            {"name": "URL", "value": item["html_url"]},
                            {
                                "name": "Created At",
                                "value": format_dt(
                                    ciso8601.parse_datetime(item["created_at"])
                                ),
                            },
                            {
                                "name": "Published At",
                                "value": format_dt(
                                    ciso8601.parse_datetime(item["published_at"])
                                ),
                            },
                            {"name": "Tarball URL", "value": item["tarball_url"]},
                            {"name": "Zip URL", "value": item["zipball_url"]},
                            {
                                "name": "Download URL",
                                "value": [
                                    subItems["browser_download_url"]
                                    for subItems in item["assets"]
                                ],
                            },
                            {
                                "name": "Download Count",
                                "value": str(
                                    [
                                        subItems["download_count"]
                                        for subItems in item["assets"]
                                    ]
                                ).replace("'", ""),
                            },
                        ],
                    }
                    for item in data
                ]
                embed_source = EmbedListSource(main_data, per_page=1)
                pages = KumikoPages(source=embed_source, ctx=ctx)
                await pages.start()

    @github.command(name="repo")
    @app_commands.describe(owner="The owner of the repo", repo="The repo to search")
    async def search(self, ctx: commands.Context, owner: str, repo: str) -> None:
        """Searches for one repo on GitHub"""
        headers = {
            "Authorization": f"token {GITHUB_API_KEY}",
            "accept": "application/vnd.github.v3+json",
        }
        async with self.session.get(
            f"https://api.github.com/repos/{owner}/{repo}", headers=headers
        ) as r:
            data = await r.json(loads=orjson.loads)
            if r.status == 404:
                await ctx.send("The repo was not found")
                return
            else:
                embed = Embed(title=data["name"], description=data["description"])
                embed.set_thumbnail(url=data["owner"]["avatar_url"])
                embed.add_field(name="Fork?", value=data["fork"])
                embed.add_field(name="Private", value=data["private"])
                embed.add_field(name="Stars", value=data["stargazers_count"])
                embed.add_field(
                    name="Language",
                    value=data["language"] if data["language"] is not None else "None",
                )
                embed.add_field(name="URL", value=data["html_url"])
                embed.add_field(
                    name="Homepage",
                    value=data["homepage"] if data["homepage"] is not None else "None",
                )
                embed.add_field(
                    name="Created At",
                    value=format_dt(ciso8601.parse_datetime(data["created_at"])),
                )
                embed.add_field(
                    name="Updated At",
                    value=format_dt(ciso8601.parse_datetime(data["updated_at"])),
                )
                embed.add_field(
                    name="Pushed At",
                    value=format_dt(ciso8601.parse_datetime(data["pushed_at"])),
                )
                await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Github(bot))
