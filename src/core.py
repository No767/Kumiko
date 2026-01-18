from __future__ import annotations

import asyncio
import contextlib
import gzip
import importlib
import inspect
import itertools
import logging
import os
import shutil
import sys
import uuid
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TypeVar, Union, overload

import discord
import msgspec
import orjson
import zstandard
from async_lru import alru_cache
from discord import app_commands
from discord.ext import commands, menus

from cogs import EXTENSIONS, VERSION
from cogs.ext import prometheus
from utils.checks import is_docker
from utils.context import KumikoContext
from utils.embeds import Embed
from utils.pages import KumikoPages

try:
    from watchfiles import Change, awatch
except ImportError:
    _HAS_WATCHFILES = False

    raise RuntimeError("Watchfiles is not installed")
else:
    _HAS_WATCHFILES = True

if TYPE_CHECKING:
    from collections.abc import Mapping
    from types import TracebackType

    import asyncpg
    from aiohttp import ClientSession

__description__ = (
    "A personal multipurpose Discord bot built with freedom and choice in mind"
)

T = TypeVar("T")

### Application core function utilities


def find_config() -> Optional[Path]:
    try:
        cred_dir = Path(os.environ["CREDENTIALS_DIRECTORY"]) / "bot_config"

        return cred_dir.resolve()
    except KeyError:
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


### Discord-specific function overrides


@alru_cache(maxsize=512)
async def get_prefix(bot: Kumiko, message: discord.Message) -> str | list[str]:
    """Obtains the prefix for the guild

    This coroutine is heavily cached in order to reduce database calls
    and improved performance


    Args:
        bot (Kumiko): An instance of `Kumiko`
        message (discord.Message): The message that is processed

    Returns:
        str | list[str]: The default prefix or a list of prefixes (including the default)
    """
    user_id = bot.user.id  # type: ignore

    # By putting the base with the mentions, we are effectively
    # doing the exact same thing as commands.when_mentioned
    base = [f"<@!{user_id}> ", f"<@{user_id}> ", bot.default_prefix]
    if message.guild is None:
        get_prefix.cache_invalidate(bot, message)
        return base

    query = """
    SELECT ARRAY_AGG(guild_prefixes.prefix) AS prefixes
    FROM guilds
    INNER JOIN guild_prefixes ON guilds.id = guild_prefixes.guild_id
    WHERE guilds.id = $1;
    """
    prefixes = await bot.pool.fetchval(query, message.guild.id)
    if prefixes is None:
        get_prefix.cache_invalidate(bot, message)
        return base

    base.extend(set(prefixes))
    return base


### Application configuration


class PrometheusSettings(msgspec.Struct, frozen=True):
    enabled: bool
    host: str
    port: int


class KumikoConfig(msgspec.Struct, frozen=True):
    token: str
    dev_mode: bool
    prometheus: PrometheusSettings
    postgres_uri: str

    @classmethod
    def load_from_file(cls, path: Optional[Path]) -> KumikoConfig:
        if not path:
            raise FileNotFoundError("Configuration file not found")

        with path.open() as f:
            return msgspec.yaml.decode(f.read(), type=KumikoConfig)


### Application development utilities


class Reloader:
    def __init__(self, bot: Kumiko, root_path: Path) -> None:
        self.bot = bot
        self.loop = asyncio.get_running_loop()
        self.root_path = root_path
        self.logger = self.bot.logger
        self._cogs_path = self.root_path / "cogs"
        self._utils_path = self.root_path / "utils"

    def reload_utils_modules(self, module: str) -> None:
        try:
            actual_module = sys.modules[module]
            importlib.reload(actual_module)
        except KeyError:
            self.logger.warning("Failed to reload module %s. Does it exist?", module)

    def find_modules_from_path(self, path: str) -> Optional[str]:
        root, ext = os.path.splitext(path)  # noqa: PTH122
        if ext != ".py":
            return None
        return ".".join(root.split("/")[1:])

    def find_true_module(self, module: str) -> str:
        parts = module.split(".")
        if "utils" in parts:
            utils_index = parts.index("utils")
            return ".".join(parts[utils_index:])
        cog_index = parts.index("cogs")
        return ".".join(parts[cog_index:])

    async def reload_or_load_extension(self, module: str) -> None:
        try:
            await self.bot.reload_extension(module)
            self.logger.info("Reloaded extension: %s", module)
        except commands.ExtensionNotLoaded:
            await self.bot.load_extension(module)
            self.logger.info("Loaded extension: %s", module)

    async def reload_cogs_and_utils(self, ctype: Change, true_module: str) -> None:
        if true_module.startswith("cogs"):
            if ctype in (Change.modified, Change.added):
                await self.reload_or_load_extension(true_module)
            elif ctype == Change.deleted:
                await self.bot.unload_extension(true_module)
        elif true_module.startswith("utils"):
            self.logger.info("Reloaded utils module: %s", true_module)
            self.reload_utils_modules(true_module)

    async def _watch_cogs(self):
        async for changes in awatch(self._cogs_path, self._utils_path, recursive=True):
            for ctype, cpath in changes:
                module = self.find_modules_from_path(cpath)
                if module is None:
                    continue

                true_module = self.find_true_module(module)
                await self.reload_cogs_and_utils(ctype, true_module)

    def start(self) -> None:
        if _HAS_WATCHFILES:
            self.loop.create_task(self._watch_cogs())
            self.bot.dispatch("reloader_ready")


### Application core utilities


class Blacklist[T]:
    """Internal blacklist database used by R. Danny"""

    def __init__(
        self,
        filepath: Path,
        *,
        load_later: bool = False,
    ) -> None:
        self.filepath = filepath
        self.encoder = msgspec.json.Encoder()
        self.loop = asyncio.get_running_loop()
        self.lock = asyncio.Lock()
        self._db: dict[str, Union[T, Any]] = {}
        if load_later:
            self.loop.create_task(self.load())
        else:
            self.load_from_file()

    def load_from_file(self) -> None:
        try:
            with self.filepath.open(mode="r", encoding="utf-8") as f:
                self._db = msgspec.json.decode(f.read())
        except FileNotFoundError:
            self._db = {}

    async def load(self) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self.load_from_file)

    def _dump(self):
        temp_id = uuid.uuid4()
        temp_file = Path(f"{temp_id}-{self.filepath.name}.tmp")

        systemd_state = os.getenv("STATE_DIRECTORY")

        if systemd_state:
            temp_file = Path(systemd_state) / temp_file

        with temp_file.open("w", encoding="utf-8") as tmp:
            encoded = msgspec.json.format(
                self.encoder.encode(self._db.copy()), indent=2
            )
            tmp.write(encoded.decode())

        # atomically move the file
        temp_file.replace(self.filepath)

    async def save(self) -> None:
        async with self.lock:
            await self.loop.run_in_executor(None, self._dump)

    @overload
    def get(self, key: Any) -> Optional[Union[T, Any]]: ...

    @overload
    def get(self, key: Any, default: Any) -> Union[T, Any]: ...

    def get(self, key: Any, default: Any = None) -> Optional[Union[T, Any]]:
        """Retrieves a config entry."""
        return self._db.get(str(key), default)

    async def put(self, key: Any, value: Union[T, Any]) -> None:
        """Edits a config entry."""
        self._db[str(key)] = value
        await self.save()

    async def remove(self, key: Any) -> None:
        """Removes a config entry."""
        del self._db[str(key)]
        await self.save()

    def __contains__(self, item: Any) -> bool:
        return str(item) in self._db

    def __getitem__(self, item: Any) -> Union[T, Any]:
        return self._db[str(item)]

    def __len__(self) -> int:
        return len(self._db)

    def all(self) -> dict[str, Union[T, Any]]:
        return self._db


class CompressionRotatingFileHandler(RotatingFileHandler):
    MAX_BYTES = 32 * 1024 * 1024  # 32 MiB
    BACKUP_COUNT = 5

    def __init__(self, *, use_zstd: Optional[bool] = False) -> None:
        self.use_zstd = use_zstd

        self.rotator = self._rotator
        self.namer = self._namer

        super().__init__(
            filename=self._determine_filename(),
            encoding="utf-8",
            mode="w",
            maxBytes=self.MAX_BYTES,
            backupCount=self.BACKUP_COUNT,
        )

    def _determine_filename(self) -> Path:
        try:
            # Checks for whether systemd's log directory is set. If set, send the logs to /var/lib/kumiko
            logs_dir = Path(os.environ["LOGS_DIRECTORY"]) / "kumiko.log"
            return logs_dir.resolve()

        except KeyError:
            logs_parent_dir = Path("logs/kumiko.log").parent

            if not logs_parent_dir.exists():
                logs_parent_dir.mkdir()

            final_logs_dir = logs_parent_dir / "kumiko.log"
            return final_logs_dir.resolve()

    def _namer(self, name: str) -> str:
        if self.use_zstd:
            return name + ".zst"
        return name + ".gz"

    def _rotator(self, source: str, dest: str) -> None:
        with Path.open(source, mode="rb") as f_source:
            if self.use_zstd:
                with zstandard.open(dest, "wb") as f_dest:
                    shutil.copyfileobj(f_source, f_dest)
            else:
                with gzip.open(dest, "wb") as f_dest:
                    shutil.copyfileobj(f_source, f_dest)

        Path.unlink(source)


class KumikoLogger:
    def __init__(self) -> None:
        self._disable_watchfiles_logger()

        self.root = logging.getLogger("kumiko")

    def _get_formatter(self) -> logging.Formatter:
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        return logging.Formatter(
            "[{asctime}] [{levelname}]\t\t{message}", dt_fmt, style="{"
        )

    def _disable_watchfiles_logger(self) -> None:
        watchfiles = logging.getLogger("watchfiles")

        watchfiles.propagate = False
        watchfiles.addHandler(logging.NullHandler())

    def __enter__(self) -> None:
        discord_logger = logging.getLogger("discord")

        handler = logging.StreamHandler()
        handler.setFormatter(self._get_formatter())

        if not is_docker():
            file_handler = CompressionRotatingFileHandler()
            file_handler.setFormatter(self._get_formatter())

            discord_logger.addHandler(file_handler)
            self.root.addHandler(file_handler)

        discord_logger.setLevel(logging.INFO)
        discord_logger.addHandler(handler)

        self.root.setLevel(logging.INFO)
        self.root.addHandler(handler)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.root.info("Shutting down...")
        handlers = self.root.handlers[:]

        for handler in handlers:
            handler.close()
            self.root.removeHandler(handler)


class KeyboardInterruptHandler:
    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot
        self._task: Optional[asyncio.Task] = None

    def __call__(self) -> None:
        if self._task:
            raise KeyboardInterrupt
        self._task = self.bot.loop.create_task(self.bot.close())


### Discord-specific overrides

#### Help Menu

# RGB Colors:
# Pink (255, 161, 231) - Used for the main bot page
# Lavender (197, 184, 255) - Used for cog and group pages
# Light Orange (255, 199, 184) - Used for command pages


def process_perms_name(
    command: Union[commands.Group, commands.Command],
) -> Optional[str]:
    merge_list = []
    if (
        all(isinstance(parent, commands.Group) for parent in command.parents)
        and len(command.parents) > 0
    ):
        # See https://stackoverflow.com/a/27638751
        merge_list = [
            next(iter(parent.extras["permissions"])) for parent in command.parents
        ]

    if "permissions" in command.extras:
        merge_list.extend([*command.extras["permissions"]])

    perms_set = sorted(set(merge_list))
    if len(perms_set) == 0:
        return None
    return ", ".join(name.replace("_", " ").title() for name in perms_set)


class GroupHelpPageSource(menus.ListPageSource):
    def __init__(
        self,
        group: Union[commands.Group, commands.Cog],
        entries: list[commands.Command],
        *,
        prefix: str,
    ) -> None:
        super().__init__(entries=entries, per_page=6)
        self.group: Union[commands.Group, commands.Cog] = group
        self.prefix: str = prefix
        self.title: str = f"{self.group.qualified_name} Commands"
        self.description: str = self.group.description

    def _process_description(self, group: Union[commands.Group, commands.Cog]) -> str:
        if isinstance(group, commands.Group) and "permissions" in group.extras:
            return f"{self.description}\n\n**Required Permissions**: {process_perms_name(group)}"
        return self.description

    async def format_page(  # type: ignore
        self, menu: KumikoPages, commands: list[commands.Command]
    ) -> Embed:
        embed = Embed(
            title=self.title,
            description=self._process_description(self.group),
            colour=discord.Colour.from_rgb(197, 184, 255),
        )

        for command in commands:
            signature = f"{command.qualified_name} {command.signature}"
            embed.add_field(
                name=signature,
                value=command.short_doc or "No help given...",
                inline=False,
            )

        maximum = self.get_max_pages()
        if maximum > 1:
            embed.set_author(
                name=f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} commands)"
            )

        embed.set_footer(
            text=f'Use "{self.prefix}help command" for more info on a command.'
        )
        return embed


class HelpSelectMenu(discord.ui.Select["HelpMenu"]):
    def __init__(
        self, entries: dict[commands.Cog, list[commands.Command]], bot: Kumiko
    ) -> None:
        super().__init__(
            placeholder="Select a category...",
            min_values=1,
            max_values=1,
            row=0,
        )
        self.cmds: dict[commands.Cog, list[commands.Command]] = entries
        self.bot = bot
        self.__fill_options()

    def __fill_options(self) -> None:
        self.add_option(
            label="Index",
            emoji="\N{WAVING HAND SIGN}",
            value="__index",
            description="The help page showing how to use the bot.",
        )
        for cog, cmds in self.cmds.items():
            if not cmds:
                continue
            description = cog.description.split("\n", 1)[0] or None
            emoji = getattr(cog, "display_emoji", None)
            self.add_option(
                label=cog.qualified_name,
                value=cog.qualified_name,
                description=description,
                emoji=emoji,
            )

    async def callback(self, interaction: discord.Interaction) -> None:
        if self.view is not None:
            value = self.values[0]
            if value == "__index":
                await self.view.rebind(FrontPageSource(), interaction)
            else:
                cog = self.bot.get_cog(value)
                if cog is None:
                    await interaction.response.send_message(
                        "Somehow this category does not exist?", ephemeral=True
                    )
                    return

                commands = self.cmds[cog]
                if not commands:
                    await interaction.response.send_message(
                        "This category has no commands for you", ephemeral=True
                    )
                    return

                source = GroupHelpPageSource(
                    cog, commands, prefix=self.view.ctx.clean_prefix
                )
                await self.view.rebind(source, interaction)


class HelpMenu(KumikoPages):
    def __init__(self, source: menus.PageSource, ctx: commands.Context) -> None:
        super().__init__(source, ctx=ctx, compact=True)

    def add_categories(
        self, commands: dict[commands.Cog, list[commands.Command]]
    ) -> None:
        self.clear_items()
        self.add_item(HelpSelectMenu(commands, self.ctx.bot))
        self.fill_items()

    async def rebind(
        self, source: menus.PageSource, interaction: discord.Interaction
    ) -> None:
        self.source = source
        self.current_page = 0

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self.get_kwargs_from_page(page)
        self._update_labels(0)
        await interaction.response.edit_message(**kwargs, view=self)


class FrontPageSource(menus.PageSource):
    def is_paginating(self) -> bool:
        # This forces the buttons to appear even in the front page
        return True

    def get_max_pages(self) -> Optional[int]:  # type: ignore
        # There's only one actual page in the front page
        # However we need at least 2 to show all the buttons
        return 2

    async def get_page(self, page_number: int) -> Any:
        # The front page is a dummy
        self.index = page_number
        return self

    async def format_page(self, menu: HelpMenu, page: Any) -> Embed:
        embed = Embed(title="Bot Help", colour=discord.Colour.from_rgb(255, 161, 231))
        embed.description = inspect.cleandoc(
            f"""
            Hello! Welcome to the help page.

            Use "{menu.ctx.clean_prefix}help command" for more info on a command.
            Use "{menu.ctx.clean_prefix}help category" for more info on a category.
            Use the dropdown menu below to select a category.
        """
        )

        embed.add_field(
            name="Support Server",
            value="For more help, consider joining the official server over at https://discord.gg/ns3e74frqn",
            inline=False,
        )

        if self.index == 0:
            embed.add_field(
                name="About Kumiko",
                value=(
                    "Kumiko is an multipurpose bot that takes an unique and alternative approach to "
                    "what an multipurpose bot is. Kumiko offers features such as a redirects system, quiet mode, and many more. You can get more "
                    "information on the commands offered by using the dropdown below.\n\n"
                    "Kumiko is also open source. You can see the code on [GitHub](https://github.com/No767/Kumiko)"
                ),
                inline=False,
            )
        elif self.index == 1:
            entries = (
                ("<argument>", "This means the argument is __**required**__."),
                ("[argument]", "This means the argument is __**optional**__."),
                ("[A|B]", "This means that it can be __**either A or B**__."),
                (
                    "[argument...]",
                    "This means you can have multiple arguments.\n"
                    "Now that you know the basics, it should be noted that...\n"
                    "__**You do not type in the brackets!**__",
                ),
            )

            embed.add_field(
                name="How do I use this bot?",
                value="Reading the bot signature is pretty simple.",
            )

            for name, value in entries:
                embed.add_field(name=name, value=value, inline=False)

        return embed


class KumikoHelp(commands.HelpCommand):
    context: commands.Context

    def __init__(self) -> None:
        super().__init__(
            command_attrs={
                "cooldown": commands.CooldownMapping.from_cooldown(
                    1, 3.0, commands.BucketType.member
                ),
                "help": "Shows help about the bot, a command, or a category",
            }
        )

    async def on_help_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, commands.CommandInvokeError):
            # Ignore missing permission errors
            if (
                isinstance(error.original, discord.HTTPException)
                and error.original.code == 50013
            ):
                return

            await ctx.send(str(error.original))

    def get_command_signature(self, command: commands.Command) -> str:
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    async def send_bot_help(
        self, mapping: Mapping[Optional[commands.Cog], list[commands.Command]]
    ) -> None:
        bot = self.context.bot

        def key(command: commands.Command) -> str:
            cog = command.cog
            return cog.qualified_name if cog else "\U0010ffff"

        entries: list[commands.Command] = await self.filter_commands(
            bot.commands, sort=True, key=key
        )

        all_commands: dict[commands.Cog, list[commands.Command]] = {}
        for name, children in itertools.groupby(entries, key=key):
            if name == "\U0010ffff":
                continue

            cog = bot.get_cog(name)
            if cog is not None:
                all_commands[cog] = sorted(children, key=lambda c: c.qualified_name)

        menu = HelpMenu(FrontPageSource(), ctx=self.context)
        menu.add_categories(all_commands)
        await menu.start()

    async def send_cog_help(self, cog: commands.Cog) -> None:
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        menu = HelpMenu(
            GroupHelpPageSource(cog, entries, prefix=self.context.clean_prefix),
            ctx=self.context,
        )
        await menu.start()

    def common_command_formatting(
        self,
        embed_like: Union[discord.Embed, GroupHelpPageSource],
        command: commands.Command,
    ) -> None:
        embed_like.title = self.get_command_signature(command)
        processed_perms = process_perms_name(command)
        if isinstance(embed_like, discord.Embed) and processed_perms is not None:
            embed_like.add_field(name="Required Permissions", value=processed_perms)

        if command.description:
            embed_like.description = f"{command.description}\n\n{command.help}"
        else:
            embed_like.description = command.help or "No help found..."

    async def send_command_help(self, command: commands.Command) -> None:
        # No pagination necessary for a single command.
        embed = discord.Embed(colour=discord.Colour.from_rgb(255, 199, 184))
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def send_group_help(self, group: commands.Group) -> None:
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        if len(entries) == 0:
            return await self.send_command_help(group)

        source = GroupHelpPageSource(group, entries, prefix=self.context.clean_prefix)
        self.common_command_formatting(source, group)
        menu = HelpMenu(source, ctx=self.context)
        await menu.start()
        return None


#### Command Tree


class KumikoCommandTree(app_commands.CommandTree):
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        bot: Kumiko = interaction.client  # type: ignore # Checked and it is that
        if interaction.user.id in (bot.owner_id, bot.application_id):
            return True

        if interaction.user.id in bot.blacklist:
            bot.metrics.blacklist.commands.inc(1)
            msg = (
                f"My fellow user, {interaction.user.mention}, you just got the L. "
                "You are blacklisted from using this bot. Take an \U0001f1f1, \U0001f1f1oser. "
                "[Here is your appeal form](https://media.tenor.com/K9R9beOgPR4AAAAC/fortnite-thanos.gif)"
            )
            await interaction.response.send_message(msg, ephemeral=True)
            return False

        if interaction.guild and interaction.guild.id in bot.blacklist:
            bot.metrics.blacklist.commands.inc(1)
            await interaction.response.send_message(
                "This is so sad lolllllll! Your whole entire server got blacklisted!",
                ephemeral=True,
            )
            return False

        bot.metrics.commands.invocation.inc()
        if interaction.command:
            name = interaction.command.qualified_name
            bot.metrics.commands.count.labels(name).inc()

        return True


class Kumiko(commands.Bot):
    FILE_ROOT = Path(__file__).parent

    """The core of Kumiko - Subclassed this time"""

    def __init__(
        self,
        config: KumikoConfig,
        session: ClientSession,
        pool: asyncpg.Pool,
    ) -> None:
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
            description=__description__,
            help_command=KumikoHelp(),
            intents=intents,
            tree_cls=KumikoCommandTree,
        )
        self.blacklist: Blacklist[bool] = Blacklist(self._determine_blacklist_path())
        self.default_prefix = ">"
        self.logger: logging.Logger = logging.getLogger("kumiko")
        self.metrics = prometheus.MetricCollector(self)
        self.pool = pool
        self.session = session
        self.version = str(VERSION)

        self._config = config
        self._reloader = Reloader(self, self.FILE_ROOT)

        self._dev_mode = config.dev_mode
        self._prometheus = config.prometheus

    ### Blacklist utilities

    def _determine_blacklist_path(self) -> Path:
        try:
            return Path(os.environ["STATE_DIRECTORY"]) / "blacklist.json"
        except KeyError:
            return self.FILE_ROOT.parent / "blacklist.json"

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

        if self._prometheus.enabled:
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

        if self._prometheus.enabled and not hasattr(self, "guild_metrics_created"):
            self.guild_metrics_created = self.metrics.guilds.fill()

        user = None if self.user is None else self.user.name
        self.logger.info("%s is fully ready!", user)

    async def on_reloader_ready(self) -> None:
        self.logger.info("Dev mode is enabled. Loaded Reloader")
