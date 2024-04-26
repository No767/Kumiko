from typing import Optional

import discord
from discord.ext import commands
from typing_extensions import Annotated

from .utils import TimeoutDTConverter


class BanFlags(commands.FlagConverter):
    member: discord.Member = commands.flag(
        aliases=["m"], description="The member to ban"
    )
    delete_messages: bool = commands.flag(
        aliases=["delm"],
        default=True,
        description="Automatically purges messages that the user has sent",
    )
    reason: str = commands.flag(
        aliases=["r"], default=None, description="The reason for banning said user(s)"
    )


class KickFlags(commands.FlagConverter):
    member: discord.Member = commands.flag(
        aliases=["m"], description="The member to kick"
    )
    reason: str = commands.flag(
        aliases=["r"], default=None, description="The reason for kicking said user(s)"
    )


class TimeoutFlags(commands.FlagConverter):
    member: discord.Member = commands.flag(
        aliases=["m"], description="The member to timeout"
    )
    duration: Optional[Annotated[str, TimeoutDTConverter]] = commands.flag(
        aliases=["d"],
        default=None,
        description="The duration to timeout the user(s) for. Leave this out in order to remove the timeout",
    )
    reason: str = commands.flag(
        aliases=["r"], default=None, description="The reason for issuing the timeout"
    )
