from discord.ext import commands
from Libs.errors import PinsDisabledError

from .pin_utils import get_or_fetch_enabled_status


async def check_pin_enabled(ctx: commands.Context):
    if ctx.guild is None:
        raise PinsDisabledError
    res = await get_or_fetch_enabled_status(
        ctx.guild.id, ctx.bot.pool, ctx.bot.redis_pool
    )
    if res is None or res is False:
        raise PinsDisabledError
    return res


def is_pins_enabled():
    async def pred(ctx: commands.Context):
        return await check_pin_enabled(ctx)

    return commands.check(pred)
