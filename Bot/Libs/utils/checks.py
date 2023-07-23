from __future__ import annotations

from typing import Callable, TypeVar

from discord import app_commands
from discord.ext import commands

T = TypeVar("T")

# For time's sake I might as well take these from RDanny
# There is really no used of creating my own system when there is one out there already
async def check_guild_permissions(
    ctx: commands.Context, perms: dict[str, bool], *, check=all
):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    resolved = ctx.author.guild_permissions  # type: ignore
    return check(
        getattr(resolved, name, None) == value for name, value in perms.items()
    )


def hybrid_permissions_check(**perms: bool) -> Callable[[T], T]:
    async def pred(ctx: commands.Context):
        return await check_guild_permissions(ctx, perms)

    def decorator(func: T) -> T:
        commands.check(pred)(func)
        app_commands.default_permissions(**perms)(func)
        return func

    return decorator


def is_manager():
    return hybrid_permissions_check(manage_guild=True)


def is_mod():
    return hybrid_permissions_check(
        ban_members=True, manage_messages=True, kick_members=True, moderate_members=True
    )


def is_admin():
    return hybrid_permissions_check(administrator=True)
