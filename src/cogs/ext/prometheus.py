from __future__ import annotations

import platform
from typing import TYPE_CHECKING, NamedTuple

import discord
from discord.ext import commands, tasks

try:
    from prometheus_async.aio.web import start_http_server
    from prometheus_client import Counter, Enum, Gauge, Info, Summary
except ImportError:
    raise RuntimeError(
        "Prometheus libraries are required to be installed. "
        "Either install those libraries or disable Prometheus extension"
    )


if TYPE_CHECKING:
    from core import Kumiko


METRIC_PREFIX = "discord_"


class GuildCount(NamedTuple):
    amount: int
    text: int
    voice: int
    users: int


class GuildCollector:
    __slots__ = ("amount", "bot", "text", "users", "voice")

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot
        self.amount = Gauge(f"{METRIC_PREFIX}guilds", "Amount of guilds connected")
        self.text = Gauge(
            f"{METRIC_PREFIX}text", "Amount of text channels that can be seen"
        )
        self.voice = Gauge(f"{METRIC_PREFIX}voice", "Amount of voice channels")
        self.users = Gauge(f"{METRIC_PREFIX}users", "Total users")

    def _get_stats(self) -> GuildCount:
        users = 0
        text = 0
        voice = 0
        guilds = 0
        for guild in self.bot.guilds:
            guilds += 1
            if guild.unavailable:
                continue

            users += guild.member_count or 0

            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text += 1
                elif isinstance(channel, discord.VoiceChannel):
                    voice += 1

        return GuildCount(amount=guilds, text=text, voice=voice, users=users)

    def fill(self) -> None:
        stats = self._get_stats()

        self.amount.set(stats.amount)
        self.text.set(stats.text)
        self.voice.set(stats.voice)
        self.users.set(stats.users)


class BlacklistCollector:
    __slots__ = ("bot", "commands", "users")

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot

        # For now, until we can improve the blacklist system,
        # we will leave these to be blank
        self.users = Gauge(
            f"{METRIC_PREFIX}blacklist_users", "Current amount of blacklisted users"
        )
        self.commands = Counter(
            f"{METRIC_PREFIX}blacklist_commands",
            "Counter of commands that were attempted for blacklisted users",
        )
        self.fill()

    def fill(self) -> None:
        self.users.set(len(self.bot.blacklist.all()))


class FeatureCollector:
    __slots__ = ("bot", "successful_redirects")

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot
        self.successful_redirects = Counter(
            f"{METRIC_PREFIX}successful_redirects",
            "Counter of successful redirects invocations",
        )


class CommandsCollector:
    __slots__ = ("bot", "count", "invocation", "total")

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot

        self.total = Summary(
            f"{METRIC_PREFIX}commands_total", "Total commands included"
        )
        self.invocation = Counter(
            f"{METRIC_PREFIX}commands_invocation",
            "Counter for invoked prefix and slash commands",
        )
        self.count = Counter(
            f"{METRIC_PREFIX}commands_count",
            "Individual count for commands",
            ["commands"],
        )

    def fill(self, amount: int) -> None:
        self.total.observe(amount)


class MetricCollector:
    __slots__ = (
        "blacklist",
        "bot",
        "commands",
        "connected",
        "features",
        "guilds",
        "latency",
        "version",
    )

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot

        self.connected = Enum(
            f"{METRIC_PREFIX}connected",
            "Connected to Discord",
            ["shard"],
            states=["connected", "disconnected"],
        )
        self.latency = Gauge(f"{METRIC_PREFIX}latency", "Latency to Discord", ["shard"])
        self.version = Info(f"{METRIC_PREFIX}version", "Versions of the bot")
        self.commands = CommandsCollector(bot)
        self.guilds = GuildCollector(bot)
        self.blacklist = BlacklistCollector(bot)
        self.features = FeatureCollector(bot)

    def _get_commands(self) -> int:
        total = 0

        for _ in self.bot.walk_commands():
            total += 1

        return total

    def fill(self) -> None:
        self.version.info(
            {
                "build_version": self.bot.version,
                "dpy_version": discord.__version__,
                "python_version": platform.python_version(),
            }
        )
        self.commands.fill(self._get_commands())

    async def start(self, host: str, port: int) -> None:
        await start_http_server(addr=host, port=port)


class Prometheus(commands.Cog):
    """Cog which handles Prometheus metrics for Kumiko"""

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot
        self._connected_label = self.bot.metrics.connected.labels(None)

    async def cog_load(self) -> None:
        # For some reason it would only work inside here
        self.latency_loop.start()

    async def cog_unload(self) -> None:
        self.latency_loop.stop()

    @tasks.loop(seconds=5)
    async def latency_loop(self) -> None:
        self.bot.metrics.latency.labels(None).set(self.bot.latency)

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        self._connected_label.state("connected")

    @commands.Cog.listener()
    async def on_resumed(self) -> None:
        self._connected_label.state("connected")

    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        self._connected_label.state("disconnected")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        self.bot.metrics.guilds.fill()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        self.bot.metrics.guilds.fill()


async def setup(bot: Kumiko) -> None:
    await bot.add_cog(Prometheus(bot))
