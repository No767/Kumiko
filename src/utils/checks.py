from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import discord
from discord import app_commands
from discord.ext import commands

# Although commands.HybridCommand (and it's group version) can be bound here for Type T,
# it doesn't make sense as they are just subclasses of commands.Command and co.
T = TypeVar("T", commands.Command, commands.Group)

if TYPE_CHECKING:
    from collections.abc import Callable

    from utils.context import KumikoContext


async def check_guild_permissions(
    ctx: KumikoContext, perms: dict[str, bool], *, check: bool = all
) -> bool:
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    resolved = ctx.author.guild_permissions  # type: ignore
    return check(
        getattr(resolved, name, None) == value for name, value in perms.items()
    )


async def check_bot_permissions(
    ctx: KumikoContext, perms: dict[str, bool], *, check: bool = all
) -> bool:
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    bot_resolved_perms = ctx.me.guild_permissions  # type: ignore
    return check(
        getattr(bot_resolved_perms, name, None) == value
        for name, value in perms.items()
    )


def check_permissions(**perms: bool) -> Callable[[T], T]:
    async def pred(ctx: KumikoContext):
        # Usually means this is in the context of a DM
        if (
            isinstance(ctx.me, discord.ClientUser)
            or isinstance(ctx.author, discord.User)
            or ctx.guild is None
        ):
            return False
        guild_perms = await check_guild_permissions(ctx, perms)
        can_run = ctx.me.top_role > ctx.author.top_role
        return guild_perms and can_run

    def decorator(func: T) -> T:
        func.extras["permissions"] = perms
        commands.check(pred)(func)
        app_commands.default_permissions(**perms)(func)
        return func

    return decorator


def bot_check_permissions(**perms: bool) -> Callable[[T], T]:
    async def pred(ctx: KumikoContext):
        return await check_bot_permissions(ctx, perms)

    def decorator(func: T) -> T:
        commands.check(pred)(func)
        app_commands.default_permissions(**perms)(func)
        return func

    return decorator


def is_manager() -> Callable[[T], T]:
    return check_permissions(manage_guild=True)


def is_mod() -> Callable[[T], T]:
    return check_permissions(
        ban_members=True,
        manage_messages=True,
        kick_members=True,
        moderate_members=True,
    )


def is_admin() -> Callable[[T], T]:
    return check_permissions(administrator=True)


def is_docker() -> bool:
    """Checks if the current environment is running in Docker

    Returns:
        bool: Returns `True` if in fact it is an Docker environment,
        `False` if not
    """
    path = Path("/proc/self/cgroup")
    dockerenv_path = Path("/.dockerenv")
    return dockerenv_path.exists() or (
        path.is_file() and any("docker" in line for line in path.open())
    )
