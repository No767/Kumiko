from discord.ext import commands


class EventsFlag(commands.FlagConverter):
    all: bool = commands.flag(
        default=False, override=True, description="Whether to enable all events"
    )
