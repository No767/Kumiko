from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from libs.config import GuildCacheHandler
from libs.errors import RedirectsDisabledError

if TYPE_CHECKING:
    from bot.kumiko import KumikoCore


def check_if_thread(ctx: commands.Context):
    return isinstance(ctx.channel, discord.Thread) and not isinstance(
        ctx.channel, discord.ForumChannel
    )


def is_thread():
    def pred(ctx: commands.Context):
        return check_if_thread(ctx)

    return commands.check(pred)


async def check_redirects_enabled(ctx: commands.Context):
    if ctx.guild is None:
        raise RedirectsDisabledError

    cache = GuildCacheHandler(ctx.guild.id, ctx.bot.redis_pool)
    status = await cache.get_value(".config.redirects")
    if not isinstance(status, bool) or status is False:
        raise RedirectsDisabledError
    return status


async def check_redirects_menu(interaction: discord.Interaction):
    if interaction.guild is None:
        return False

    bot: KumikoCore = interaction.client  # type: ignore
    cache = GuildCacheHandler(interaction.guild.id, bot.redis_pool)
    status = await cache.get_value(".config.redirects")
    if not isinstance(status, bool) or status is False:
        return False
    return status
