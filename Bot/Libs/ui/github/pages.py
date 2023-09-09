from typing import Any, List, Optional

import discord
from discord.ext import commands, menus
from discord.utils import utcnow
from Libs.utils import MessageConstants
from Libs.utils.pages import EmbedListSource, KumikoPages

from .page_entries import GitHubIssuesCommentsPageEntry, GitHubUserPageEntry
from .structs import GitHubIssue, GitHubIssueComment
from .utils import parse_state


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
