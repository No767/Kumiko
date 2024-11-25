import logging
from pathlib import Path
from typing import Union

import asyncpg
import discord
import orjson
from aiohttp import ClientSession
from cogs import EXTENSIONS, VERSION
from discord.ext import commands
from libs.utils.config import KumikoConfig
from libs.utils.context import KumikoContext
from libs.utils.help import KumikoHelpPaginated
from libs.utils.prefix import get_prefix
from libs.utils.reloader import Reloader
from libs.utils.tree import KumikoCommandTree


async def init(conn: asyncpg.Connection):
    # Refer to https://github.com/MagicStack/asyncpg/issues/140#issuecomment-301477123
    def _encode_jsonb(value):
        return b"\x01" + orjson.dumps(value)

    def _decode_jsonb(value):
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
        intents: discord.Intents,
        session: ClientSession,
        pool: asyncpg.Pool,
        *args,
        **kwargs,
    ):
        super().__init__(
            intents=intents,
            command_prefix=get_prefix,
            help_command=KumikoHelpPaginated(),
            activity=discord.Activity(type=discord.ActivityType.watching, name=">help"),
            tree_cls=KumikoCommandTree,
            *args,
            **kwargs,
        )
        self.config = config
        self.default_prefix = ">"
        self.logger: logging.Logger = logging.getLogger("kumiko")
        self.pool = pool
        self.session = session
        self.version = str(VERSION)
        self._config = config
        self._dev_mode = config.kumiko.get("dev_mode", False)
        self._reloader = Reloader(self, Path(__file__).parent)

    ### Bot-related overrides

    # Need to override context for custom ones
    # for now, we can just use the default commands.Context
    async def get_context(
        self,
        origin: Union[discord.Interaction, discord.Message],
        /,
        *,
        cls=KumikoContext,
    ) -> KumikoContext:
        return await super().get_context(origin, cls=cls)

    async def on_command_error(
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

        # TODO - Add Blacklist Feature

        await self.invoke(ctx)

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)

    ### Internal core overrides

    async def setup_hook(self) -> None:
        for cog in EXTENSIONS:
            self.logger.debug(f"Loaded extension: {cog}")
            await self.load_extension(cog)

        await self.load_extension("jishaku")

        if self._dev_mode:
            self._reloader.start()

    async def on_ready(self) -> None:
        if not hasattr(self, "uptime"):
            self.uptime = discord.utils.utcnow()
        curr_user = None if self.user is None else self.user.name
        self.logger.info(f"{curr_user} is fully ready!")

    async def on_reloader_ready(self) -> None:
        self.logger.info("Dev mode is enabled. Loaded Reloader")