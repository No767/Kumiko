import traceback

import discord
from discord.ext import commands

from .embeds import ErrorEmbed


def produce_error_embed(error: Exception) -> ErrorEmbed:
    """Produces a standard error embed

    Args:
        error (Exception): The error

    Returns:
        ErrorEmbed: An `ErrorEmbed` instance with the standard preset
    """
    error_traceback = "\n".join(traceback.format_exception_only(type(error), error))
    embed = ErrorEmbed()
    desc = f"""
    Uh oh! It seems like there was an issue. For support, please visit [Kumiko's Support Server](https://discord.gg/ns3e74frqn) to get help!
    
    **Error**:
    ```{error_traceback}```
    """
    embed.description = desc
    embed.set_footer(text="Happened At")
    embed.timestamp = discord.utils.utcnow()
    return embed


def build_cooldown_embed(error: commands.CommandOnCooldown) -> ErrorEmbed:
    embed = ErrorEmbed()
    embed.timestamp = discord.utils.utcnow()
    embed.title = "Command On Cooldown"
    embed.description = (
        f"This command is on cooldown. Try again in {error.retry_after:.2f}s"
    )
    return embed


def create_premade_embed(title: str, description: str) -> ErrorEmbed:
    embed = ErrorEmbed()
    embed.timestamp = discord.utils.utcnow()
    embed.title = title
    embed.description = description
    return embed


async def send_error_embed(ctx: commands.Context, error: commands.CommandError) -> None:
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=build_cooldown_embed(error))
    elif isinstance(error, commands.CommandInvokeError) or isinstance(
        error, commands.HybridCommandError
    ):
        await ctx.send(embed=produce_error_embed(error))
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send(
            embed=create_premade_embed(
                "Guild Only", "This command cannot be used in private messages"
            )
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            embed=create_premade_embed(
                "Missing Required Argument",
                f"You are missing the following argument(s): {error.param.name}",
            )
        )
