import discord
from discord.ext import commands
from Libs.config import GuildCacheHandler
from Libs.errors import RedirectsDisabledError


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


def is_redirects_enabled():
    async def pred(ctx: commands.Context):
        return await check_redirects_enabled(ctx)

    return commands.check(pred)
