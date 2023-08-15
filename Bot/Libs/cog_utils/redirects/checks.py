import discord
from discord.ext import commands
from Libs.errors import RedirectsDisabledError

from .utils import get_or_fetch_status


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
    status = await get_or_fetch_status(ctx.guild.id, ctx.bot.pool, ctx.bot.redis_pool)
    if status is None:
        raise RedirectsDisabledError
    elif status is False:
        raise RedirectsDisabledError
    return status


def is_redirects_enabled():
    async def pred(ctx: commands.Context):
        return await check_redirects_enabled(ctx)

    return commands.check(pred)
