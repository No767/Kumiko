from discord.ext import commands


class EventsFlag(commands.FlagConverter):
    member: bool = commands.flag(
        default=True,
        aliases=["member_events"],
        description="Whether to enable member events",
    )
    mod: bool = commands.flag(
        default=True, aliases=["mod_events"], description="Whether to enable mod events"
    )
    eco: bool = commands.flag(
        default=True,
        aliases=["eco_events"],
        description="Whether to enable economy events",
    )
    all: bool = commands.flag(
        default=False, override=True, description="Whether to enable all events"
    )
