from __future__ import annotations

import datetime
import re
from typing import TYPE_CHECKING, Any, Optional, Sequence, Union

import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from discord.ext import commands
from typing_extensions import Self

if TYPE_CHECKING:
    from libs.utils.context import KContext


class ShortTime:
    compiled = re.compile(
        """
           (?:(?P<years>[0-9])(?:years?|y))?                      # e.g. 2y
           (?:(?P<months>[0-9]{1,2})(?:months?|mon?))?            # e.g. 2months
           (?:(?P<weeks>[0-9]{1,4})(?:weeks?|w))?                 # e.g. 10w
           (?:(?P<days>[0-9]{1,5})(?:days?|d))?                   # e.g. 14d
           (?:(?P<hours>[0-9]{1,5})(?:hours?|hr?s?))?             # e.g. 12h
           (?:(?P<minutes>[0-9]{1,5})(?:minutes?|m(?:ins?)?))?    # e.g. 10m
           (?:(?P<seconds>[0-9]{1,5})(?:seconds?|s(?:ecs?)?))?    # e.g. 15s
        """,
        re.VERBOSE,
    )

    discord_fmt = re.compile(r"<t:(?P<ts>[0-9]+)(?:\:?[RFfDdTt])?>")

    dt: datetime.datetime

    def __init__(
        self,
        argument: str,
        *,
        now: Optional[datetime.datetime] = None,
        tzinfo: datetime.tzinfo = datetime.timezone.utc,
    ):
        match = self.compiled.fullmatch(argument)
        if match is None or not match.group(0):
            match = self.discord_fmt.fullmatch(argument)
            if match is not None:
                self.dt = datetime.datetime.fromtimestamp(
                    int(match.group("ts")), tz=datetime.timezone.utc
                )
                if tzinfo is not datetime.timezone.utc:
                    self.dt = self.dt.astimezone(tzinfo)
                return
            else:
                raise commands.BadArgument("invalid time provided")

        data = {k: int(v) for k, v in match.groupdict(default=0).items()}
        now = now or datetime.datetime.now(datetime.timezone.utc)
        self.dt = now + relativedelta(dt1=None, dt2=None, **data)
        if tzinfo is not datetime.timezone.utc:
            self.dt = self.dt.astimezone(tzinfo)

    @classmethod
    async def convert(cls, ctx: KContext, argument: str) -> Self:
        tzinfo = datetime.timezone.utc
        return cls(argument, now=ctx.message.created_at, tzinfo=tzinfo)


class HumanTime:
    calendar = pdt.Calendar(version=pdt.VERSION_CONTEXT_STYLE)

    def __init__(
        self,
        argument: str,
        *,
        now: Optional[datetime.datetime] = None,
        tzinfo: datetime.tzinfo = datetime.timezone.utc,
    ):
        now = now or datetime.datetime.now(tzinfo)
        dt, status = self.calendar.parseDT(argument, sourceTime=now, tzinfo=None)
        if not isinstance(status, int):
            if not status.hasDateOrTime:
                raise commands.BadArgument(
                    'Invalid time provided, try e.g. "tomorrow" or "3 days"'
                )

            if not status.hasTime:
                # replace it with the current time
                dt = dt.replace(
                    hour=now.hour,
                    minute=now.minute,
                    second=now.second,
                    microsecond=now.microsecond,
                )

        self.dt: datetime.datetime = dt.replace(tzinfo=tzinfo)
        if now.tzinfo is None:
            now = now.replace(tzinfo=datetime.timezone.utc)
        self._past: bool = self.dt < now

    @classmethod
    async def convert(cls, ctx: KContext, argument: str) -> Self:
        tzinfo = datetime.timezone.utc
        return cls(argument, now=ctx.message.created_at, tzinfo=tzinfo)


class FriendlyTimeResult:
    dt: datetime.datetime
    arg: str

    __slots__ = ("dt", "arg")

    def __init__(self, dt: datetime.datetime):
        self.dt = dt
        self.arg = ""

    async def ensure_constraints(
        self,
        ctx: KContext,
        uft: UserFriendlyTime,
        now: datetime.datetime,
        remaining: str,
    ) -> None:
        if self.dt < now:
            raise commands.BadArgument("This time is in the past.")

        if not remaining:
            if uft.default is None:
                raise commands.BadArgument("Missing argument after the time.")
            remaining = uft.default

        if uft.converter is not None:
            self.arg = await uft.converter.convert(ctx, remaining)
        else:
            self.arg = remaining


# Pulling from R. Danny so I don't waste my time
# Also apparently modmail just copied this for some reason...
# https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/utils/time.py#L210C1-L324C22
class UserFriendlyTime(commands.Converter):
    """That way quotes aren't absolutely necessary."""

    def __init__(
        self,
        converter: Optional[Union[type[commands.Converter], commands.Converter]] = None,
        *,
        default: Any = None,
    ):
        if isinstance(converter, type) and issubclass(converter, commands.Converter):
            converter = converter()

        if converter is not None and not isinstance(converter, commands.Converter):
            raise TypeError("commands.Converter subclass necessary.")

        self.converter: commands.Converter = converter  # type: ignore  # It doesn't understand this narrowing
        self.default: Any = default

    async def convert(self, ctx: KContext, argument: str) -> FriendlyTimeResult:
        calendar = HumanTime.calendar
        regex = ShortTime.compiled
        now = ctx.message.created_at

        tzinfo = datetime.timezone.utc

        match = regex.match(argument)
        if match is not None and match.group(0):
            data = {k: int(v) for k, v in match.groupdict(default=0).items()}
            remaining = argument[match.end() :].strip()
            dt = now + relativedelta(dt1=None, dt2=None, **data)
            result = FriendlyTimeResult(dt.astimezone(tzinfo))
            await result.ensure_constraints(ctx, self, now, remaining)
            return result

        if match is None or not match.group(0):
            match = ShortTime.discord_fmt.match(argument)
            if match is not None:
                result = FriendlyTimeResult(
                    datetime.datetime.fromtimestamp(
                        int(match.group("ts")), tz=datetime.timezone.utc
                    ).astimezone(tzinfo)
                )
                remaining = argument[match.end() :].strip()
                await result.ensure_constraints(ctx, self, now, remaining)
                return result

        # apparently nlp does not like "from now"
        # it likes "from x" in other cases though so let me handle the 'now' case
        if argument.endswith("from now"):
            argument = argument[:-8].strip()

        if argument[0:2] == "me":
            # starts with "me to", "me in", or "me at "
            if argument[0:6] in ("me to ", "me in ", "me at "):
                argument = argument[6:]

        # Have to adjust the timezone so pdt knows how to handle things like "tomorrow at 6pm" in an aware way
        now = now.astimezone(tzinfo)
        elements = calendar.nlp(argument, sourceTime=now)
        if elements is None or len(elements) == 0:
            raise commands.BadArgument(
                'Invalid time provided, try e.g. "tomorrow" or "3 days".'
            )

        # handle the following cases:
        # "date time" foo
        # date time foo
        # foo date time

        # first the first two cases:
        dt, status, begin, end, _ = elements[0]

        if not status.hasDateOrTime:
            raise commands.BadArgument(
                'Invalid time provided, try e.g. "tomorrow" or "3 days".'
            )

        if begin not in (0, 1) and end != len(argument):
            raise commands.BadArgument(
                "Time is either in an inappropriate location, which "
                "must be either at the end or beginning of your input, "
                "or I just flat out did not understand what you meant. Sorry."
            )

        dt = dt.replace(tzinfo=tzinfo)
        if not status.hasTime:
            # replace it with the current time
            dt = dt.replace(
                hour=now.hour,
                minute=now.minute,
                second=now.second,
                microsecond=now.microsecond,
            )

        if status.hasTime and not status.hasDate and dt < now:
            # if it's in the past, and it has a time but no date,
            # assume it's for the next occurrence of that time
            dt = dt + datetime.timedelta(days=1)

        # if midnight is provided, just default to next day
        if status.accuracy == pdt.pdtContext.ACU_HALFDAY:
            dt = dt + datetime.timedelta(days=1)

        result = FriendlyTimeResult(dt)
        remaining = ""

        if begin in (0, 1):
            if begin == 1:
                # check if it's quoted:
                if argument[0] != '"':
                    raise commands.BadArgument("Expected quote before time input...")

                if not (end < len(argument) and argument[end] == '"'):
                    raise commands.BadArgument(
                        "If the time is quoted, you must unquote it."
                    )

                remaining = argument[end + 1 :].lstrip(" ,.!")
            else:
                remaining = argument[end:].lstrip(" ,.!")
        elif len(argument) == end:
            remaining = argument[:begin].strip()

        await result.ensure_constraints(ctx, self, now, remaining)
        return result


class Plural:
    def __init__(self, value: int):
        self.value: int = value

    def __format__(self, format_spec: str) -> str:
        v = self.value
        singular, _, plural = format_spec.partition("|")
        plural = plural or f"{singular}s"
        if abs(v) != 1:
            return f"{v} {plural}"
        return f"{v} {singular}"


def human_join(seq: Sequence[str], delim: str = ", ", final: str = "or") -> str:
    size = len(seq)
    if size == 0:
        return ""

    if size == 1:
        return seq[0]

    if size == 2:
        return f"{seq[0]} {final} {seq[1]}"

    return delim.join(seq[:-1]) + f" {final} {seq[-1]}"


# The old system does work, but as noted, can be inaccurate
# This system is from RDanny and should provide more accurate results
def human_timedelta(
    dt: datetime.datetime,
    *,
    source: Optional[datetime.datetime] = None,
    accuracy: Optional[int] = 3,
    brief: bool = False,
    suffix: bool = True,
) -> str:
    now = source or datetime.datetime.now(datetime.timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)

    if now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)

    # Microsecond free zone
    now = now.replace(microsecond=0)
    dt = dt.replace(microsecond=0)

    # This implementation uses relativedelta instead of the much more obvious
    # divmod approach with seconds because the seconds approach is not entirely
    # accurate once you go over 1 week in terms of accuracy since you have to
    # hardcode a month as 30 or 31 days.
    # A query like "11 months" can be interpreted as "!1 months and 6 days"
    if dt > now:
        delta = relativedelta(dt, now)
        output_suffix = ""
    else:
        delta = relativedelta(now, dt)
        output_suffix = " ago" if suffix else ""

    attrs = [
        ("year", "y"),
        ("month", "mo"),
        ("day", "d"),
        ("hour", "h"),
        ("minute", "m"),
        ("second", "s"),
    ]

    output = []
    for attr, brief_attr in attrs:
        elem = getattr(delta, attr + "s")
        if not elem:
            continue

        if attr == "day":
            weeks = delta.weeks
            if weeks:
                elem -= weeks * 7
                if not brief:
                    output.append(format(Plural(weeks), "week"))
                else:
                    output.append(f"{weeks}w")

        if elem <= 0:
            continue

        if brief:
            output.append(f"{elem}{brief_attr}")
        else:
            output.append(format(Plural(elem), attr))

    if accuracy is not None:
        output = output[:accuracy]

    if len(output) == 0:
        return "now"
    else:
        if not brief:
            return human_join(output, final="and") + output_suffix
        else:
            return " ".join(output) + output_suffix
