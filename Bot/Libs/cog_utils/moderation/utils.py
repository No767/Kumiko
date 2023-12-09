import datetime

from discord.ext import commands
from discord.utils import utcnow
from Libs.utils import parse_dt
from Libs.utils.context import GuildContext

# from typing import TYPE_CHECKING


class TimeoutDTConverter(commands.Converter):
    async def convert(self, ctx: GuildContext, argument: str):
        parsed_arg = parse_dt(argument)
        now = utcnow()

        if parsed_arg is None:
            raise commands.BadArgument("Cannot parse datetime argument")

        # Basically if the TZ is actually not None, then we wil assume the TZ given
        # By default, it will be UTC
        parsed_arg_cleaned = parsed_arg.astimezone(datetime.timezone.utc)

        if parsed_arg.tzinfo is not None:
            parsed_arg_cleaned = parsed_arg.astimezone(parsed_arg.tzinfo)

        time_diff = parsed_arg_cleaned - now
        max_time = datetime.timedelta(days=28)

        if time_diff > max_time:
            raise commands.BadArgument(
                "Timeout cannot be more than 28 days from the given date."
            )

        return parsed_arg_cleaned
