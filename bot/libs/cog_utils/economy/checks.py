from discord.ext import commands
from libs.config import GuildCacheHandler
from libs.errors import EconomyDisabledError


async def check_economy_enabled(ctx: commands.Context) -> bool:
    if ctx.guild is None:
        raise EconomyDisabledError

    cache = GuildCacheHandler(ctx.guild.id, ctx.bot.redis_pool)
    res = await cache.get_value(".config.local_economy")

    if not isinstance(res, bool) or res is False:
        raise EconomyDisabledError
    return res


def is_economy_enabled():
    async def pred(ctx: commands.Context):
        return await check_economy_enabled(ctx)

    return commands.check(pred)
