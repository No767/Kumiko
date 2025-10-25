import contextlib
import logging
from pathlib import Path
from typing import Any, Optional, Union

import asyncpg
import discord
import orjson
from aiohttp import ClientSession
from discord.ext import commands

from cogs import EXTENSIONS, VERSION
from cogs.ext import prometheus
from utils.config import Blacklist, KumikoConfig
from utils.context import KumikoContext
from utils.help import KumikoHelp
from utils.prefix import get_prefix
from utils.reloader import _HAS_WATCHFILES, Reloader
from utils.tree import KumikoCommandTree

description = (
    "A personal multipurpose Discord bot built with freedom and choice in mind"
)


def find_config() -> Optional[Path]:
    path = Path("config.yml")

    if not path.exists():
        alt_location = path.parent.joinpath("src", "config.yml")

        if not alt_location.exists():
            return None

        return alt_location.resolve()

    return path.resolve()


async def init(conn: asyncpg.Connection) -> None:
    # Refer to https://github.com/MagicStack/asyncpg/issues/140#issuecomment-301477123
    def _encode_jsonb(value: Any):
        return b"\x01" + orjson.dumps(value)

    def _decode_jsonb(value: Any):
        return orjson.loads(value[1:].decode("utf-8"))

    await conn.set_type_codec(
        "jsonb",
        schema="pg_catalog",
        encoder=_encode_jsonb,
        decoder=_decode_jsonb,
        format="binary",
    )


class Kumiko(commands.Bot):
    """The core of Kumiko - Subclassed this time"""

    def __init__(
        self,
        config: KumikoConfig,
        session: ClientSession,
        pool: asyncpg.Pool,
        **kwargs,
    ):
        intents = discord.Intents(
            emojis=True,
            guilds=True,
            message_content=True,
            messages=True,
            reactions=True,
            voice_states=True,
        )
        super().__init__(
            activity=discord.Activity(type=discord.ActivityType.watching, name=">help"),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, replied_user=False
            ),
            command_prefix=get_prefix,
            description=description,
            help_command=KumikoHelp(),
            intents=intents,
            tree_cls=KumikoCommandTree,
            **kwargs,
        )
        self.blacklist: Blacklist[bool] = Blacklist(
            Path(__file__).parent / "blacklist.json"
        )
        self.default_prefix = ">"
        self.logger: logging.Logger = logging.getLogger("kumiko")
        self.metrics = prometheus.MetricCollector(self)
        self.pool = pool
        self.session = session
        self.version = str(VERSION)
        self._config = config
        self._dev_mode = config.dev_mode
        self._reloader = Reloader(self, Path(__file__).parent)
        self._prometheus = config.prometheus
        self._prometheus_enabled = self._prometheus.enabled

    ### Blacklist utilities

    async def add_to_blacklist(self, object_id: int) -> None:
        await self.blacklist.put(object_id, True)

    async def remove_from_blacklist(self, object_id: int) -> None:
        with contextlib.suppress(KeyError):
            await self.blacklist.remove(object_id)

    ### Bot-related overrides

    # Need to override context for custom ones
    # for now, we can just use the default commands.Context
    async def get_context(  # type: ignore
        self,
        origin: Union[discord.Interaction, discord.Message],
        /,
        *,
        cls: KumikoContext = KumikoContext,
    ) -> KumikoContext:
        return await super().get_context(origin, cls=cls)

    async def on_command_error(  # type: ignore
        self, ctx: KumikoContext, error: commands.CommandError
    ) -> None:
        if self._dev_mode:
            self.logger.exception("Ignoring exception:", exc_info=error)
            return

        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send("This command cannot be used in private messages")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"You are missing the following argument(s): {error.param.name}"
            )
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                self.logger.exception(
                    "In %s:",
                    ctx.command.qualified_name,  # type: ignore
                    exc_info=original,
                )
        elif isinstance(error, commands.BadArgument):
            await ctx.send(str(error))

    async def process_commands(self, message: discord.Message) -> None:
        ctx = await self.get_context(message)

        if ctx.command is None:
            return

        if ctx.author.id in self.blacklist:
            self.metrics.blacklist.commands.inc(1)
            return

        if ctx.guild and ctx.guild.id in self.blacklist:
            self.metrics.blacklist.commands.inc(1)
            return

        # Guaranteed to be commands now
        self.metrics.commands.invocation.inc()
        name = ctx.command.qualified_name
        self.metrics.commands.count.labels(name).inc()

        await self.invoke(ctx)

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_guild_join(self, guild: discord.Guild) -> None:
        if guild.id in self.blacklist:
            await guild.leave()

    ### Internal core overrides

    async def setup_hook(self) -> None:
        for cog in EXTENSIONS:
            self.logger.debug("Loaded extension: %s", cog)
            await self.load_extension(cog)

        await self.load_extension("jishaku")

        if self._prometheus_enabled:
            await self.load_extension("cogs.ext.prometheus")
            prom_host = self._prometheus.host
            prom_port = self._prometheus.port

            await self.metrics.start(host=prom_host, port=prom_port)
            self.logger.info("Prometheus Server started on %s:%s", prom_host, prom_port)

            self.metrics.fill()

        if self._dev_mode and _HAS_WATCHFILES:
            self._reloader.start()

    async def on_ready(self) -> None:
        if not hasattr(self, "uptime"):
            self.uptime = discord.utils.utcnow()

        if self._prometheus_enabled and not hasattr(self, "guild_metrics_created"):
            self.guild_metrics_created = self.metrics.guilds.fill()

        user = None if self.user is None else self.user.name
        self.logger.info("%s is fully ready!", user)

    async def on_reloader_ready(self) -> None:
        self.logger.info("Dev mode is enabled. Loaded Reloader")
