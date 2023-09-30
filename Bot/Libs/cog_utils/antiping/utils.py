from __future__ import annotations

from typing import TYPE_CHECKING, Union

import asyncpg
import discord

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore


async def get_antiping_user(
    bot: KumikoCore, user: Union[discord.User, discord.Member], pool: asyncpg.Pool
):
    if user.id in bot.antiping_cache:
        return bot.antiping_cache[user.id]
