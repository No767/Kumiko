from __future__ import annotations

import datetime
import itertools
import platform
from typing import TYPE_CHECKING, Optional, Union

import discord
import psutil
import pygit2
from dateutil.relativedelta import relativedelta
from discord.ext import commands
from pygit2.enums import SortMode

from utils.checks import is_docker
from utils.embeds import Embed

if TYPE_CHECKING:
    from collections.abc import Sequence

    from core import Kumiko


def human_timedelta(
    dt: datetime.datetime,
    *,
    source: Optional[datetime.datetime] = None,
    accuracy: Optional[int] = 3,
    brief: bool = False,
    suffix: bool = True,
) -> str:
    def _human_join(seq: Sequence[str], delim: str = ", ", final: str = "or") -> str:
        if not seq:
            return ""
        if len(seq) == 1:
            return seq[0]
        return f"{delim.join(seq[:-1])} {final} {seq[-1]}"

    now = source or datetime.datetime.now(datetime.UTC)

    # Merge timezone checks
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.UTC)
    if now.tzinfo is None:
        now = now.replace(tzinfo=datetime.UTC)

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

        # Handle weeks logic inside the 'day' iteration
        if attr == "day" and delta.weeks:
            weeks = delta.weeks
            elem -= weeks * 7
            output.append(f"{weeks}w" if brief else format(Plural(weeks), "week"))

        # Skip if elem is <= 0 (specifically for days after week subtraction)
        if elem <= 0:
            continue

        # Merged formatting logic
        output.append(f"{elem}{brief_attr}" if brief else format(Plural(elem), attr))

    if accuracy is not None:
        output = output[:accuracy]

    if not output:
        return "now"

    if brief:
        return " ".join(output) + output_suffix

    return _human_join(output, final="and") + output_suffix


class Plural:
    def __init__(self, value: int) -> None:
        self.value: int = value

    def __format__(self, format_spec: str) -> str:
        v = self.value
        singular, _, plural = format_spec.partition("|")
        plural = plural or f"{singular}s"
        if abs(v) != 1:
            return f"{v} {plural}"
        return f"{v} {singular}"


class Meta(commands.Cog):
    """Commands to obtain info about Kumiko or others"""

    def __init__(self, bot: Kumiko) -> None:
        self.bot = bot
        self.process = psutil.Process()

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U00002754")

    def _format_date(self, dt: Optional[datetime.datetime]) -> str:
        if not dt:
            return "N/A"
        return (
            f"{discord.utils.format_dt(dt, 'F')} ({discord.utils.format_dt(dt, 'R')})"
        )

    def _format_commit(self, commit: pygit2.Commit) -> str:
        short, _, _ = commit.message.partition("\n")
        short_sha2 = str(commit.id)[0:6]
        commit_tz = datetime.timezone(
            datetime.timedelta(minutes=commit.commit_time_offset)
        )
        commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(
            commit_tz
        )

        # [`hash`](url) message (offset)
        offset = discord.utils.format_dt(commit_time.astimezone(datetime.UTC), "R")
        commit_id = str(commit.id)
        return f"[`{short_sha2}`](https://github.com/No767/Kumiko/commit/{commit_id}) {short} ({offset})"

    def _get_last_commits(self, count: int = 5):
        repo = pygit2.Repository(".git")
        commits = list(
            itertools.islice(repo.walk(repo.head.target, SortMode.TOPOLOGICAL), count)
        )
        return "\n".join(self._format_commit(c) for c in commits)

    def _get_bot_uptime(self, *, brief: bool = False) -> str:
        return human_timedelta(
            self.bot.uptime, accuracy=None, brief=brief, suffix=False
        )

    @commands.hybrid_command(name="uptime")
    async def uptime(self, ctx: commands.Context) -> None:
        """Returns uptime for Kumiko"""
        embed = Embed()
        embed.description = f"Kumiko's Uptime: **{self._get_bot_uptime()}**"
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="info")
    async def info(
        self, ctx: commands.Context, *, user: Union[discord.Member, discord.User]
    ) -> None:
        """Shows info about a user"""
        user = user or ctx.author

        status_str = ""
        if isinstance(user, discord.Member):
            status_lookup = [
                ("\U0001f5a5", user.desktop_status),
                ("\U0001f4f1", user.mobile_status),
                ("\U0001f310", user.web_status),
            ]
            status_str = "".join(
                [item[0] for item in status_lookup if item[1] == discord.Status.online]
            )

        platform_status = (
            f"**Platform Statuses**: {status_str}" if len(status_str) != 0 else ""
        )

        roles = []
        if ctx.guild is not None and isinstance(user, discord.Member):
            roles = [role.name.replace("@", "@\u200b") for role in user.roles]

        desc = f"""
        **Name/ID**: {user.global_name} / {user.id}
        **Created**: {self._format_date(user.created_at)}
        **Status**: {user.status if isinstance(user, discord.Member) else "Unknown"}
        {platform_status}
        **Mutual Guilds**: {len(user.mutual_guilds)}
        **Roles**: {", ".join(roles)}
        """

        embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))
        embed.set_author(name=user.global_name, icon_url=user.display_avatar.url)
        embed.description = desc
        embed.timestamp = user.joined_at if isinstance(user, discord.Member) else None
        embed.set_footer(text="Joined at")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="about")
    async def about(self, ctx: commands.Context) -> None:
        """Shows info and stats about Kumiko"""
        total_members = 0
        total_unique = len(self.bot.users)

        guilds = 0
        for guild in self.bot.guilds:
            guilds += 1
            if guild.unavailable:
                continue

            total_members += guild.member_count or 0

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()  # type: ignore # I'm not sure why pyright is complaining about this

        revisions = self._get_last_commits()

        if is_docker():
            revisions = "See [GitHub](https://github.com/No767/Kumiko)"

        embed = Embed()
        embed.set_author(
            name=self.bot.user.name,  # type: ignore
            icon_url=self.bot.user.display_avatar.url,  # type: ignore
        )
        embed.title = "Support Server Invite"
        embed.url = "https://discord.gg/ns3e74frqn"
        embed.description = (
            "Kumiko is a personal multipurpose bot that takes an unique and alternative approach to what an multipurpose bot is. "
            "Features include the redirects system, quiet mode, and many more.\n\n"
            f"Latest Changes:\n {revisions}"
        )
        embed.set_footer(
            text=f"Made with discord.py v{discord.__version__} | Running Python {platform.python_version()}",
            icon_url="https://cdn.discordapp.com/emojis/596577034537402378.png?size=100",
        )
        embed.add_field(name="Guilds", value=guilds)
        embed.add_field(
            name="Users", value=f"{total_members} total\n{total_unique} unique"
        )
        embed.add_field(
            name="Process", value=f"{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU"
        )
        embed.add_field(name="Python Version", value=platform.python_version())
        embed.add_field(name="Kumiko Version", value=str(self.bot.version))
        embed.add_field(name="Uptime", value=self._get_bot_uptime(brief=True))
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version")
    async def version(self, ctx: commands.Context) -> None:
        """Returns the current version of Kumiko"""
        embed = Embed()
        embed.description = f"Build Version: {self.bot.version!s}"
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="invite")
    async def invite(self, ctx: commands.Context) -> None:
        """Invite Kumiko to your server!"""
        if self.bot.application_id is None:
            return
        perms = discord.Permissions()
        perms.kick_members = True
        perms.ban_members = True
        perms.moderate_members = True
        perms.manage_messages = True
        perms.send_messages_in_threads = True
        perms.manage_threads = True
        perms.create_public_threads = True
        perms.embed_links = True
        perms.read_message_history = True
        perms.external_emojis = True
        perms.add_reactions = True
        url = discord.utils.oauth_url(self.bot.application_id, permissions=perms)
        await ctx.send(url)


async def setup(bot: Kumiko) -> None:
    await bot.add_cog(Meta(bot))
