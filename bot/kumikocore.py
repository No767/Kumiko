import logging
import signal
from pathlib import Path as SyncPath
from typing import Union

import asyncpg
import discord
from aiohttp import ClientSession
from cogs import EXTENSIONS, VERSION
from discord.ext import commands, ipcx
from libs.errors import send_error_embed
from libs.utils import (
    KContext,
    KumikoCommandTree,
    KumikoHelpPaginated,
    MessageConstants,
    get_blacklist,
)
from libs.utils.config import KumikoConfig
from libs.utils.prefix import get_prefix
from redis.asyncio.connection import ConnectionPool

# Some weird import logic to ensure that watchfiles is there
_fsw = True
try:
    from watchfiles import awatch
except ImportError:
    _fsw = False


class KumikoCore(commands.Bot):
    """The core of Kumiko - Subclassed this time"""

    def __init__(
        self,
        intents: discord.Intents,
        config: KumikoConfig,
        session: ClientSession,
        pool: asyncpg.Pool,
        redis_pool: ConnectionPool,
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
        self.ipc = ipcx.Server(
            self,
            host=config["postgres_uri"],
            secret_key=config["postgres_uri"],
        )
        self.logger: logging.Logger = logging.getLogger("kumiko")
        self.pool = pool
        self.redis_pool = redis_pool
        self.session = session
        self.version = str(VERSION)
        self._dev_mode = config["kumiko"].get("dev_mode", False)

    async def _fs_watcher(self) -> None:
        cogs_path = SyncPath(__file__).parent.joinpath("Cogs")
        async for changes in awatch(cogs_path):
            changes_list = list(changes)[0]
            if changes_list[0].modified == 2:
                reload_file = SyncPath(changes_list[1])
                self.logger.info(f"Reloading extension: {reload_file.name[:-3]}")
                await self.reload_extension(f"Cogs.{reload_file.name[:-3]}")

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        await send_error_embed(ctx, error)

    # Need to override context for custom ones
    # for now, we can just use the default commands.Context
    async def get_context(
        self, origin: Union[discord.Interaction, discord.Message], /, *, cls=KContext
    ) -> KContext:
        return await super().get_context(origin, cls=cls)

    async def check_blacklist(self, ctx: KContext) -> bool:
        bot = ctx.bot  # Pretty much returns the subclass anyways. I checked - Noelle
        if bot.owner_id == ctx.author.id or bot.application_id == ctx.author.id:
            return True

        blacklist = await get_blacklist(ctx.author, ctx.guild, bot.pool)

        if blacklist is not None:
            await ctx.send(
                f"My fellow user, {ctx.author.mention}, you just got the L. {MessageConstants.BLACKLIST_APPEAL_MSG.value}",
                suppress_embeds=True,
            )
            return False
        return True

    async def setup_hook(self) -> None:
        def stop():
            self.loop.create_task(self.close())

        self.loop.add_signal_handler(signal.SIGTERM, stop)
        self.loop.add_signal_handler(signal.SIGINT, stop)

        # The blacklist checks

        for cog in EXTENSIONS:
            self.logger.debug(f"Loaded extension: {cog}")
            await self.load_extension(cog)

        await self.load_extension("jishaku")
        await self.ipc.start()

        if self._dev_mode is True and _fsw is True:
            self.logger.info("Dev mode is enabled. Loading Jishaku and FSWatcher")
            self.loop.create_task(self._fs_watcher())

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = discord.utils.utcnow()
        curr_user = None if self.user is None else self.user.name
        self.logger.info(f"{curr_user} is fully ready!")

    async def on_ipc_ready(self):
        self.logger.info(
            "Standard IPC Server started on %s:%s", self.ipc.host, self.ipc.port
        )
        self.logger.info(
            "Multicast IPC server started on %s:%s",
            self.ipc.host,
            self.ipc.multicast_port,
        )
