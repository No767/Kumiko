from discord.ext import commands

from ..utils import ErrorEmbed, produce_error_embed
from .exceptions import (
    EconomyDisabledError,
    PinsDisabledError,
    RedirectsDisabledError,
)


def create_premade_embed(title: str, description: str):
    embed = ErrorEmbed()
    embed.title = title
    embed.description = description
    return embed


async def send_error_embed(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CheckFailure) and "global check functions" in str(
        error
    ):
        return
    elif isinstance(error, commands.CommandInvokeError) or isinstance(
        error, commands.HybridCommandError
    ):
        await ctx.send(embed=produce_error_embed(error))
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(
            embed=create_premade_embed(
                "Command Not Found",
                "The command you were looking for could not be found",
            )
        )
    elif isinstance(error, commands.NotOwner):
        await ctx.send(
            embed=create_premade_embed(
                "Command requires the owner to run",
                "The command can only be ran by the owner of the guild",
            )
        )
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            embed=create_premade_embed(
                "Command on Cooldown",
                f"This command is on cooldown. Try again in {error.retry_after:.2f}s",
            )
        )
    elif isinstance(error, commands.MissingPermissions):
        missing_perms = ", ".join(error.missing_permissions).rstrip(",")
        await ctx.send(
            embed=create_premade_embed(
                "Missing Permissions",
                f"You are missing the following permissions: {missing_perms}",
            )
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            embed=create_premade_embed(
                "Missing Required Argument",
                f"You are missing the following argument(s): {error.param.name}",
            )
        )
    elif (
        isinstance(error, EconomyDisabledError)
        or isinstance(error, RedirectsDisabledError)
        or isinstance(error, PinsDisabledError)
    ):
        await ctx.send(embed=create_premade_embed(error.title, str(error)))
    else:
        await ctx.send(embed=produce_error_embed(error))
