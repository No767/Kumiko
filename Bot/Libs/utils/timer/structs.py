import datetime
from typing import Any, NamedTuple, Optional, Sequence

import asyncpg
from discord import app_commands
from discord.utils import format_dt
from typing_extensions import Self


class Timer:
    __slots__ = ("args", "kwargs", "event", "id", "created_at", "expires", "timezone")

    def __init__(self, *, record: asyncpg.Record):
        self.id: int = record["id"]

        extra = record["extra"]
        self.args: Sequence[Any] = extra.get("args", [])
        self.kwargs: dict[str, Any] = extra.get("kwargs", {})
        self.event: str = record["event"]
        self.created_at: datetime.datetime = record["created"]
        self.expires: datetime.datetime = record["expires"]
        self.timezone: str = record["timezone"]

    @classmethod
    def temporary(
        cls,
        *,
        expires: datetime.datetime,
        created: datetime.datetime,
        event: str,
        args: Sequence[Any],
        kwargs: dict[str, Any],
        timezone: str,
    ) -> Self:
        pseudo = {
            "id": None,
            "extra": {"args": args, "kwargs": kwargs},
            "event": event,
            "created": created,
            "expires": expires,
            "timezone": timezone,
        }
        return cls(record=pseudo)

    def __eq__(self, other: object) -> bool:
        try:
            return self.id == other.id  # type: ignore
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.id)

    @property
    def human_delta(self) -> str:
        return format_dt(self.created_at, "R")

    @property
    def author_id(self) -> Optional[int]:
        if self.args:
            return int(self.args[0])
        return None

    def __repr__(self) -> str:
        return f"<Timer created={self.created_at} expires={self.expires} event={self.event}>"


class TimeZone(NamedTuple):
    label: str
    key: str

    # Deal with this stuff later?
    # @classmethod
    # async def convert(cls, ctx: commands.Context, argument: str) -> Self:
    #     # assert isinstance(ctx.cog, Reminder)

    #     # Prioritise aliases because they handle short codes slightly better
    #     if argument in ctx.cog._timezone_aliases:
    #         return cls(key=ctx.cog._timezone_aliases[argument], label=argument)

    #     if argument in ctx.cog.valid_timezones:
    #         return cls(key=argument, label=argument)

    #     timezones = ctx.cog.find_timezones(argument)

    #     try:
    #         return await ctx.disambiguate(timezones, lambda t: t[0], ephemeral=True)
    #     except ValueError:
    #         raise commands.BadArgument(f'Could not find timezone for {argument!r}')

    def to_choice(self) -> app_commands.Choice[str]:
        return app_commands.Choice(name=self.label, value=self.key)
