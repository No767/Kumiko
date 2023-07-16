import asyncpg
from discord.ext import commands
from Libs.cache import KumikoCache
from Libs.errors import EconomyDisabled


def is_economy_enabled():
    async def predicate(ctx: commands.Context):
        if ctx.guild is None:
            raise EconomyDisabled
        key = f"cache:kumiko:{ctx.guild.id}:eco_status"
        cache = KumikoCache(connection_pool=ctx.bot.redis_pool)
        if await cache.cacheExists(key=key):
            result = await cache.getBasicCache(key=key)
            parsedRes = bool(int(result))  # type: ignore
            if parsedRes is False:
                raise EconomyDisabled
            return parsedRes
        else:
            pool: asyncpg.Pool = ctx.bot.pool
            res = await pool.fetchval(
                "SELECT local_economy FROM guild WHERE id = $1;", ctx.guild.id
            )
            if res is True:
                await cache.setBasicCache(key=key, value=str(1), ttl=None)
                return True
            await cache.setBasicCache(key=key, value=str(0), ttl=None)
            raise EconomyDisabled

    return commands.check(predicate)
