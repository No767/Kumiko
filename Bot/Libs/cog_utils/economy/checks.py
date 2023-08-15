from discord.ext import commands
from Libs.config import get_or_fetch_guild_config
from Libs.errors import EconomyDisabledError


async def check_economy_enabled(ctx: commands.Context):
    if ctx.guild is None:
        raise EconomyDisabledError
    res = await get_or_fetch_guild_config(
        ctx.guild.id, ctx.bot.pool, ctx.bot.redis_pool
    )
    if res is None:
        raise EconomyDisabledError
    elif res["local_economy"] is False:
        raise EconomyDisabledError
    return res["local_economy"]


def is_economy_enabled():
    async def pred(ctx: commands.Context):
        return await check_economy_enabled(ctx)

    return commands.check(pred)
