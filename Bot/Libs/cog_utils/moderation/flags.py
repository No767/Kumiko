from typing import Optional

import discord
from discord.ext import commands


class BanFlags(commands.FlagConverter):
    members: commands.Greedy[discord.Member] = commands.flag(
        aliases=["m"], default=lambda ctx: [], description="The member(s) to ban"
    )
    delete_messages: bool = commands.flag(
        aliases=["delm"],
        default=True,
        description="Automatically purges messages that the user has sent",
    )
    reason: str = commands.flag(
        aliases=["r"], default=None, description="The reason for banning said user(s)"
    )


class UnbanFlags(commands.FlagConverter):
    members: commands.Greedy[discord.Member] = commands.flag(
        aliases=["m"], default=lambda ctx: [], description="The member(s) to ban"
    )
    reason: str = commands.flag(
        aliases=["r"], default=None, description="The reason for unbanning said user(s)"
    )


class KickFlags(commands.FlagConverter):
    members: commands.Greedy[discord.Member] = commands.flag(
        aliases=["m"], default=lambda ctx: [], description="The member(s) to kick"
    )
    reason: str = commands.flag(
        aliases=["r"], default=None, description="The reason for kicking said user(s)"
    )


class TimeoutFlags(commands.FlagConverter):
    members: commands.Greedy[discord.Member] = commands.flag(
        aliases=["m"], default=lambda ctx: [], description="The member(s) to timeout"
    )
    duration: Optional[str] = commands.flag(
        aliases=["d"],
        default=None,
        description="The duration to timeout the user(s) for. Leave this out in order to remove the timeout",
    )
    reason: str = commands.flag(
        aliases=["r"], default=None, description="The reason for issuing the timeout"
    )
