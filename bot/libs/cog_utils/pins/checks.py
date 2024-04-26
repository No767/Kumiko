from discord.ext import commands
from libs.config import GuildCacheHandler
from libs.errors import PinsDisabledError


async def check_pin_enabled(ctx: commands.Context):
    if ctx.guild is None:
        raise PinsDisabledError
    cache = GuildCacheHandler(ctx.guild.id, ctx.bot.redis_pool)
    status = await cache.get_value(".config.pins")
    if not isinstance(status, bool) or status is False:
        raise PinsDisabledError
    return status


def is_pins_enabled():
    async def pred(ctx: commands.Context):
        return await check_pin_enabled(ctx)

    return commands.check(pred)
