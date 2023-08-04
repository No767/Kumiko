from typing import List

import asyncpg
from discord.ext import commands

from .base_pages import BasePages, UserInvBasePages
from .utils import (
    LeaderboardEntry,
    LeaderboardPageEntry,
    UserInvEntry,
    UserInvPageEntry,
)


class LeaderboardPages(BasePages):
    def __init__(
        self,
        entries: List[LeaderboardEntry],
        *,
        ctx: commands.Context,
        per_page: int = 10
    ):
        converted = [LeaderboardPageEntry(entry) for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx)


class UserInvPages(UserInvBasePages):
    def __init__(
        self,
        entries: List[UserInvEntry],
        *,
        ctx: commands.Context,
        per_page: int = 1,
        pool: asyncpg.Pool
    ):
        converted = [UserInvPageEntry(entry).to_dict() for entry in entries]
        super().__init__(converted, per_page=per_page, ctx=ctx, pool=pool)
