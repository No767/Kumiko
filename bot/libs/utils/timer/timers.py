from __future__ import annotations

import asyncio
import datetime
from typing import TYPE_CHECKING, Any, Optional

import asyncpg
import dateutil.tz
import discord
import fuzzy_utils as fuzzy
from async_lru import alru_cache
from dateutil.zoneinfo import get_zonefile_instance

from .structs import Timer, TimeZone
from .utils import MaybeAcquireConnection

if TYPE_CHECKING:
    from bot.kumikocore import KumikoCore


class TimerScheduler:
    """Class to access and manage timers - Pretty much ripped from R. Danny bc i'm lazy"""

    # CLDR identifiers for most common timezones for the default autocomplete drop down
    # n.b. limited to 25 choices
    DEFAULT_POPULAR_TIMEZONE_IDS = (
        # America
        "usnyc",  # America/New_York
        "uslax",  # America/Los_Angeles
        "uschi",  # America/Chicago
        "usden",  # America/Denver
        # India
        "inccu",  # Asia/Kolkata
        # Europe
        "trist",  # Europe/Istanbul
        "rumow",  # Europe/Moscow
        "gblon",  # Europe/London
        "frpar",  # Europe/Paris
        "esmad",  # Europe/Madrid
        "deber",  # Europe/Berlin
        "grath",  # Europe/Athens
        "uaiev",  # Europe/Kyev
        "itrom",  # Europe/Rome
        "nlams",  # Europe/Amsterdam
        "plwaw",  # Europe/Warsaw
        # Canada
        "cator",  # America/Toronto
        # Australia
        "aubne",  # Australia/Brisbane
        "ausyd",  # Australia/Sydney
        # Brazil
        "brsao",  # America/Sao_Paulo
        # Japan
        "jptyo",  # Asia/Tokyo
        # China
        "cnsha",  # Asia/Shanghai
    )

    def __init__(self, bot: KumikoCore):
        self.bot = bot
        self._have_data = asyncio.Event()
        self._current_timer: Optional[Timer] = None
        self._task = bot.loop.create_task(self.dispatch_timers())
        self.valid_timezones: set[str] = set(get_zonefile_instance().zones)
        # User-friendly timezone names, some manual and most from the CLDR database.
        self._timezone_aliases: dict[str, str] = {
            "Eastern Time": "America/New_York",
            "Central Time": "America/Chicago",
            "Mountain Time": "America/Denver",
            "Pacific Time": "America/Los_Angeles",
            # (Unfortunately) special case American timezone abbreviations
            "EST": "America/New_York",
            "CST": "America/Chicago",
            "MST": "America/Denver",
            "PST": "America/Los_Angeles",
            "EDT": "America/New_York",
            "CDT": "America/Chicago",
            "MDT": "America/Denver",
            "PDT": "America/Los_Angeles",
        }

    @alru_cache(maxsize=128)
    async def get_timezone(self, user_id: int, /) -> Optional[str]:
        query = "SELECT timezone from user_settings WHERE id = $1;"
        record = await self.bot.pool.fetchrow(query, user_id)
        return record["timezone"] if record else None

    async def get_tzinfo(self, user_id: int, /) -> datetime.tzinfo:
        tz = await self.get_timezone(user_id)
        if tz is None:
            return datetime.timezone.utc
        return dateutil.tz.gettz(tz) or datetime.timezone.utc

    def find_timezones(self, query: str) -> list[TimeZone]:
        # A bit hacky, but if '/' is in the query then it's looking for a raw identifier
        # otherwise it's looking for a CLDR alias
        if "/" in query:
            return [
                TimeZone(key=a, label=a)
                for a in fuzzy.finder(query, self.valid_timezones)
            ]

        keys = fuzzy.finder(query, self._timezone_aliases.keys())
        return [TimeZone(label=k, key=self._timezone_aliases[k]) for k in keys]

    async def get_active_timer(
        self, *, connection: Optional[asyncpg.Connection] = None, days: int = 7
    ) -> Optional[Timer]:
        query = """
            SELECT * FROM timers
            WHERE (expires AT TIME ZONE 'UTC' AT TIME ZONE timezone) < (CURRENT_TIMESTAMP + $1::interval)
            ORDER BY expires
            LIMIT 1;
        """
        con = connection or self.bot.pool

        record = await con.fetchrow(query, datetime.timedelta(days=days))
        return Timer(record=record) if record else None

    async def wait_for_active_timers(
        self, *, connection: Optional[asyncpg.Connection] = None, days: int = 7
    ) -> Timer:
        async with MaybeAcquireConnection(
            connection=connection, pool=self.bot.pool
        ) as con:
            timer = await self.get_active_timer(connection=con, days=days)
            if timer is not None:
                self._have_data.set()
                return timer

            self._have_data.clear()
            self._current_timer = None
            await self._have_data.wait()

            # At this point we always have data
            return await self.get_active_timer(connection=con, days=days)  # type: ignore

    async def call_timer(self, timer: Timer) -> None:
        # delete the timer
        query = "DELETE FROM reminders WHERE id=$1;"
        await self.bot.pool.execute(query, timer.id)

        # dispatch the event
        event_name = f"{timer.event}_timer_complete"
        self.bot.dispatch(event_name, timer)

    async def dispatch_timers(self) -> None:
        try:
            while not self.bot.is_closed():
                # can only asyncio.sleep for up to ~48 days reliably
                # so we're gonna cap it off at 40 days
                # see: http://bugs.python.org/issue20493
                timer = self._current_timer = await self.wait_for_active_timers(days=40)
                now = datetime.datetime.utcnow()

                if timer.expires >= now:
                    to_sleep = (timer.expires - now).total_seconds()
                    await asyncio.sleep(to_sleep)

                await self.call_timer(timer)
        except asyncio.CancelledError:
            raise
        except (OSError, discord.ConnectionClosed, asyncpg.PostgresConnectionError):
            self._task.cancel()
            self._task = self.bot.loop.create_task(self.dispatch_timers())

    async def short_timer_optimisation(self, seconds: float, timer: Timer) -> None:
        await asyncio.sleep(seconds)
        event_name = f"{timer.event}_timer_complete"
        self.bot.dispatch(event_name, timer)

    async def get_timer(self, event: str, /, **kwargs: Any) -> Optional[Timer]:
        r"""Gets a timer from the database.

        Note you cannot find a database by its expiry or creation time.

        Parameters
        -----------
        event: str
            The name of the event to search for.
        \*\*kwargs
            Keyword arguments to search for in the database.

        Returns
        --------
        Optional[:class:`Timer`]
            The timer if found, otherwise None.
        """

        filtered_clause = [
            f"extra #>> ARRAY['kwargs', '{key}'] = ${i}"
            for (i, key) in enumerate(kwargs.keys(), start=2)
        ]  # nosec # In this case it is actually needed for this to be shoved in a f-string. there is simply no way around it
        query = f"SELECT * FROM timers WHERE event = $1 AND {' AND '.join(filtered_clause)} LIMIT 1"  # nosec # see above
        record = await self.bot.pool.fetchrow(query, event, *kwargs.values())
        return Timer(record=record) if record else None

    async def delete_timer(self, event: str, /, **kwargs: Any) -> None:
        r"""Deletes a timer from the database.

        Note you cannot find a database by its expiry or creation time.

        Parameters
        -----------
        event: str
            The name of the event to search for.
        \*\*kwargs
            Keyword arguments to search for in the database.
        """

        filtered_clause = [
            f"extra #>> ARRAY['kwargs', '{key}'] = ${i}"
            for (i, key) in enumerate(kwargs.keys(), start=2)
        ]  # nosec # In this case it is actually needed for this to be shoved in a f-string. there is simply no way around it
        query = f"DELETE FROM timers WHERE event = $1 AND {' AND '.join(filtered_clause)} RETURNING id"  # nosec # see above
        record: Any = await self.bot.pool.fetchrow(query, event, *kwargs.values())

        # if the current timer is being deleted
        if (
            record is not None
            and self._current_timer
            and self._current_timer.id == record["id"]
        ):
            # cancel the task and re-run it
            self._task.cancel()
            self._task = self.bot.loop.create_task(self.dispatch_timers())

    async def create_timer(
        self, when: datetime.datetime, event: str, /, *args: Any, **kwargs: Any
    ) -> Timer:
        r"""Creates a timer.

        Parameters
        -----------
        when: datetime.datetime
            When the timer should fire.
        event: str
            The name of the event to trigger.
            Will transform to 'on_{event}_timer_complete'.
        \*args
            Arguments to pass to the event
        \*\*kwargs
            Keyword arguments to pass to the event
        connection: asyncpg.Connection
            Special keyword-only argument to use a specific connection
            for the DB request.
        created: datetime.datetime
            Special keyword-only argument to use as the creation time.
            Should make the timedeltas a bit more consistent.
        timezone: str
            Special keyword-only argument to use as the timezone for the
            expiry time. This automatically adjusts the expiry time to be
            in the future, should it be in the past.

        Note
        ------
        Arguments and keyword arguments must be JSON serialisable.

        Returns
        --------
        :class:`Timer`
        """

        pool = self.bot.pool

        try:
            now = kwargs.pop("created")
        except KeyError:
            now = discord.utils.utcnow()

        timezone_name = kwargs.pop("timezone", "UTC")
        # Remove timezone information since the database does not deal with it
        when = when.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        now = now.astimezone(datetime.timezone.utc).replace(tzinfo=None)

        timer = Timer.temporary(
            event=event,
            args=args,
            kwargs=kwargs,
            expires=when,
            created=now,
            timezone=timezone_name,
        )
        delta = (when - now).total_seconds()
        if delta <= 60:
            # a shortcut for small timers
            self.bot.loop.create_task(self.short_timer_optimisation(delta, timer))
            return timer

        query = """INSERT INTO timers (event, extra, expires, created, timezone)
                   VALUES ($1, $2::jsonb, $3, $4, $5)
                   RETURNING id;
                """

        row = await pool.fetchrow(
            query, event, {"args": args, "kwargs": kwargs}, when, now, timezone_name
        )
        timer.id = row[0]

        # only set the data check if it can be waited on
        if delta <= (86400 * 40):  # 40 days
            self._have_data.set()

        # check if this timer is earlier than our currently run timer
        if self._current_timer and when < self._current_timer.expires:
            # cancel the task and re-run it
            self._task.cancel()
            self._task = self.bot.loop.create_task(self.dispatch_timers())

        return timer
