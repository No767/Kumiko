from discord.ext import commands
from Libs.config import get_or_fetch_guild_config
from Libs.errors import EconomyDisabled


async def check_economy_enabled(ctx: commands.Context):
    if ctx.guild is None:
        raise EconomyDisabled
    res = await get_or_fetch_guild_config(
        ctx.guild.id, ctx.bot.pool, ctx.bot.redis_pool
    )
    if res is None:
        raise EconomyDisabled
    return res["local_economy"]


def is_economy_enabled():
    async def pred(ctx: commands.Context):
        return await check_economy_enabled(ctx)

    return commands.check(pred)
