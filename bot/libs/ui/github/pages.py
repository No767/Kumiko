from typing import Any, List, Optional

import discord
from discord.ext import commands, menus
from discord.utils import format_dt, utcnow
from libs.utils import MessageConstants
from libs.utils.pages import EmbedListSource, KumikoPages

from .page_entries import (
    GitHubCommitPageEntry,
    GitHubIssuesCommentsPageEntry,
    GitHubReleasePageEntry,
    GitHubUserPageEntry,
)
from .structs import (
    GitHubCommit,
    GitHubIssue,
    GitHubIssueComment,
    GitHubRepo,
    GitHubRepoReleases,
)
from .utils import parse_state, truncate_excess_string


class GitHubIssuesPageSource(menus.PageSource):
    def __init__(self, issue_entry: GitHubIssue):
        self.issue_entry = issue_entry

    def is_paginating(self) -> bool:
        # This forces the buttons to appear even in the front page
        return True

    def get_max_pages(self) -> Optional[int]:
        # There's only one actual page in the front page
        # However we need at least 2 to show all the buttons
        return 2

    async def get_page(self, page_number: int) -> Any:
        # The front page is a dummy
        self.index = page_number
        return self

    async def format_page(self, menu, page):
        ie = self.issue_entry
        menu.embed.clear_fields()
        menu.embed.set_thumbnail(url=ie.user.avatar_url)
        menu.embed.timestamp = ie.created_at or utcnow()
        menu.embed.set_footer(text="Created At")
        if self.index == 0:
            menu.embed.title = f"{parse_state(ie.state)} {ie.title}"
            menu.embed.description = ie.body or None
        elif self.index == 1:
            menu.embed.title = ie.user.name
            menu.embed.description = f"""
            **Profile URL**: {ie.user.url}
            """

        return menu.embed


class GitHubRepoPageSource(menus.PageSource):
    def __init__(self, repo_entry: GitHubRepo):
        self.repo_entry = repo_entry

    def is_paginating(self) -> bool:
        # This forces the buttons to appear even in the front page
        return True

    def get_max_pages(self) -> Optional[int]:
        # There's only one actual page in the front page
        # However we need at least 2 to show all the buttons
        return 2

    async def get_page(self, page_number: int) -> Any:
        # The front page is a dummy
        self.index = page_number
        return self

    async def format_page(self, menu, page):
        re = self.repo_entry
        menu.embed.clear_fields()
        menu.embed.set_thumbnail(url=re.owner.avatar_url)
        menu.embed.timestamp = re.created_at or utcnow()
        menu.embed.set_footer(text="Created At")
        menu.embed.title = re.full_name
        if self.index == 0:
            license = re.license.name if re.license is not None else "None"
            menu.embed.description = truncate_excess_string(re.description) or ""
            desc = f"""\n
            **------------**
            **Owner**: {re.owner.name}
            **License**: {license}
            **Language**: {re.language}
            **Stars**: {re.star_count}
            **Watchers**: {re.watchers}
            **Open Issues**: {re.open_issues}
            **URL**: {re.url}
            """
            menu.embed.description += desc
        elif self.index == 1:
            desc = f"""
            **Homepage**: {re.homepage or ''}
            **Private?**: {re.private}
            **Archived?**: {re.archived}
            **Fork?**: {re.fork}
            **Created At**: {format_dt(re.created_at)}
            **Updated At**: {format_dt(re.updated_at)}
            **Pushed At**: {format_dt(re.pushed_at)}
            **Git URL**: {re.git_url}
            **SSH URL**: {re.ssh_url}
            **Clone URL**: {re.clone_url}
            **Topics**: {','.join([item for item in re.topics]).rstrip(',')}
            """
            menu.embed.description = desc

        return menu.embed


class GitHubRepoMenu(discord.ui.Select["GithubRepoPages"]):
    def __init__(
        self, repo_entry: GitHubRepo, release_entries: List[GitHubRepoReleases]
    ):
        super().__init__(placeholder="Select a category")
        self.repo_entry = repo_entry
        self.releases_entries = release_entries

        self.__fill_options()

    def __fill_options(self):
        self.add_option(label="Repo", value="repo")
        self.add_option(label="Releases", value="releases")

    async def _send_message(self, message: str, interaction: discord.Interaction):
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
            return
        await interaction.response.send_message(message, ephemeral=True)

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view is not None
        value = self.values[0]
        if value == "repo":
            await self.view.rebind(GitHubRepoPageSource(self.repo_entry), interaction)
        else:
            if len(self.releases_entries) == 0:
                await self.view.rebind(
                    GitHubRepoPageSource(self.repo_entry), interaction
                )
                await self._send_message("There are no detected releases", interaction)
                return
            await self.view.rebind(
                EmbedListSource(
                    [
                        GitHubReleasePageEntry(entry).to_dict()
                        for entry in self.releases_entries
                    ],
                    per_page=1,
                ),
                interaction,
            )


class GitHubIssuesMenu(discord.ui.Select["GithubIssuesPages"]):
    def __init__(
        self, issue_entry: GitHubIssue, comment_entries: List[GitHubIssueComment]
    ):
        super().__init__(placeholder="Select a category")
        self.issue_entry = issue_entry
        self.comment_entries = comment_entries
        self.__fill_options()

    def __fill_options(self):
        self.add_option(label="Issue", value="issue")
        self.add_option(label="Comments", value="comments")
        self.add_option(label="Assignees", value="assignees")

    async def _send_message(self, message: str, interaction: discord.Interaction):
        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
            return
        await interaction.response.send_message(message, ephemeral=True)

    async def callback(self, interaction: discord.Interaction) -> None:
        assert self.view is not None
        value = self.values[0]
        if value == "issue":
            await self.view.rebind(
                GitHubIssuesPageSource(self.issue_entry), interaction
            )
        elif value == "comments":
            if len(self.comment_entries) == 0:
                await self.view.rebind(
                    GitHubIssuesPageSource(self.issue_entry), interaction
                )
                await self._send_message(
                    MessageConstants.NO_COMMENTS.value, interaction
                )
                return
            await self.view.rebind(
                EmbedListSource(
                    [
                        GitHubIssuesCommentsPageEntry(entry).to_dict()
                        for entry in self.comment_entries
                    ],
                    per_page=1,
                ),
                interaction,
            )
        else:
            if len(self.issue_entry.assignees) == 0:
                await self.view.rebind(
                    GitHubIssuesPageSource(self.issue_entry), interaction
                )
                await self._send_message(
                    MessageConstants.NO_ASSIGNEES.value, interaction
                )
                return
            await self.view.rebind(
                EmbedListSource(
                    [
                        GitHubUserPageEntry(entry).to_dict()
                        for entry in self.issue_entry.assignees
                    ],
                    per_page=1,
                ),
                interaction,
            )


class GithubIssuesPages(KumikoPages):
    def __init__(
        self,
        issue_entry: GitHubIssue,
        comments_entries: List[GitHubIssueComment],
        *,
        ctx: commands.Context,
        per_page: int = 1,
    ):
        self.issue_entry = issue_entry
        self.comments_entries = comments_entries
        super().__init__(GitHubIssuesPageSource(issue_entry), ctx=ctx, compact=True)
        self.add_cats()

        self.embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))

    def add_cats(self):
        self.clear_items()
        self.add_item(GitHubIssuesMenu(self.issue_entry, self.comments_entries))
        self.fill_items()

    async def rebind(
        self,
        source: menus.PageSource,
        interaction: discord.Interaction,
        to_page: int = 0,
    ) -> None:
        self.source = source
        self.current_page = 0

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self.get_kwargs_from_page(page)
        self._update_labels(0)
        await interaction.response.edit_message(**kwargs, view=self)


class GithubRepoPages(KumikoPages):
    def __init__(
        self,
        repo_entry: GitHubRepo,
        releases_entries: List[GitHubRepoReleases],
        *,
        ctx: commands.Context,
    ):
        self.repo_entry = repo_entry
        self.releases_entries = releases_entries
        super().__init__(GitHubRepoPageSource(repo_entry), ctx=ctx, compact=True)
        self.add_cats()
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))

    def add_cats(self):
        self.clear_items()
        self.add_item(GitHubRepoMenu(self.repo_entry, self.releases_entries))
        self.fill_items()

    async def rebind(
        self,
        source: menus.PageSource,
        interaction: discord.Interaction,
        to_page: int = 0,
    ) -> None:
        self.source = source
        self.current_page = 0

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self.get_kwargs_from_page(page)
        self._update_labels(0)
        await interaction.response.edit_message(**kwargs, view=self)


class GitHubCommitPages(KumikoPages):
    def __init__(self, entries: List[GitHubCommit], *, ctx: commands.Context):
        converted = [GitHubCommitPageEntry(entry).to_dict() for entry in entries]
        super().__init__(EmbedListSource(converted, per_page=1), ctx=ctx)
        self.embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))
