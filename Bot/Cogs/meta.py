import datetime
import itertools
import platform
from typing import Optional, Union

import discord
import psutil
import pygit2
from discord.ext import commands
from discord.utils import format_dt, oauth_url
from kumikocore import KumikoCore
from Libs.utils import Embed, human_timedelta, is_docker
from Libs.utils.context import KContext
from psutil._common import bytes2human


class Meta(commands.Cog):
    """Commands to obtain info about Kumiko or others"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.process = psutil.Process()

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U00002754")

    def format_date(self, dt: Optional[datetime.datetime]):
        if dt is None:
            return "N/A"
        return f'{format_dt(dt, "F")} ({format_dt(dt, "R")})'

    def format_commit(self, commit: pygit2.Commit) -> str:
        short, _, _ = commit.message.partition("\n")
        short_sha2 = commit.hex[0:6]
        commit_tz = datetime.timezone(
            datetime.timedelta(minutes=commit.commit_time_offset)
        )
        commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(
            commit_tz
        )

        # [`hash`](url) message (offset)
        offset = format_dt(commit_time.astimezone(datetime.timezone.utc), "R")
        return f"[`{short_sha2}`](https://github.com/No767/Catherine-Chan/commit/{commit.hex}) {short} ({offset})"

    def get_last_commits(self, count: int = 10):
        repo = pygit2.Repository(".git")
        commits = list(
            itertools.islice(
                repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count
            )
        )
        return "\n".join(self.format_commit(c) for c in commits)

    def get_current_branch(
        self,
    ) -> str:
        repo = pygit2.Repository(".git")
        return repo.head.shorthand

    def get_bot_uptime(self, *, brief: bool = False) -> str:
        return human_timedelta(
            self.bot.uptime, accuracy=None, brief=brief, suffix=False
        )

    @commands.hybrid_command(name="uptime")
    async def uptime(self, ctx: KContext) -> None:
        """Returns uptime for Kumiko"""
        embed = Embed()
        embed.description = f"Kumiko's Uptime: **{self.get_bot_uptime()}**"
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="info")
    async def info(
        self, ctx: KContext, *, user: Union[discord.Member, discord.User]
    ) -> None:
        """Shows info about a user"""
        user = self.bot.get_user(user.id) or (await self.bot.fetch_user(user.id))

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
        **Created**: {self.format_date(user.created_at)}
        **Status**: {user.status if isinstance(user, discord.Member) else 'Unknown'}
        {platform_status}
        **Mutual Guilds**: {len(user.mutual_guilds)}
        **Roles**: {', '.join(roles)}
        """

        embed = discord.Embed(colour=discord.Colour.from_rgb(255, 125, 212))
        embed.set_author(name=user.global_name, icon_url=user.display_avatar.url)
        embed.description = desc
        embed.timestamp = user.joined_at if isinstance(user, discord.Member) else None
        embed.set_footer(text="Joined at")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="about")
    async def about(self, ctx: KContext) -> None:
        """Shows info and stats about Kumiko"""
        total_members = 0
        total_unique = len(self.bot.users)

        text = 0
        voice = 0
        guilds = 0
        for guild in self.bot.guilds:
            guilds += 1
            if guild.unavailable:
                continue

            total_members += guild.member_count or 0
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text += 1
                elif isinstance(channel, discord.VoiceChannel):
                    voice += 1

        proc_mem = bytes2human(self.process.memory_info().rss)
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        revisions = self.get_last_commits(5)
        working_branch = self.get_current_branch().title()

        if is_docker():
            revisions = "See [GitHub](https://github.com/No767/Kumiko)"
            working_branch = "Docker"

        embed = Embed()
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url)  # type: ignore
        embed.title = "Support Server Invite"
        embed.url = "https://discord.gg/ns3e74frqn"
        embed.description = f"Latest Changes ({working_branch}):\n {revisions}"
        embed.set_footer(
            text=f"Made with discord.py v{discord.__version__} | Running Python {platform.python_version()}",
            icon_url="https://cdn.discordapp.com/emojis/596577034537402378.png?size=100",
        )
        embed.add_field(
            name="Members", value=f"{total_members} total\n{total_unique} unique"
        )
        embed.add_field(name="Channels", value=f"{text} text\n{voice} voice")
        embed.add_field(name="Guilds", value=guilds)
        embed.add_field(name="Process", value=f"{proc_mem}B \n{cpu_usage:.2f}% CPU")
        embed.add_field(name="Build Version", value=str(self.bot.version))
        embed.add_field(name="Uptime", value=self.get_bot_uptime(brief=True))
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version")
    async def version(self, ctx: KContext) -> None:
        """Returns the current version of Kumiko"""
        embed = Embed()
        embed.description = f"Build Version: {str(self.bot.version)}"
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: KContext) -> None:
        """Returns the current latency of Kumiko"""
        embed = Embed()
        embed.description = f"Pong! {round(self.bot.latency * 1000)}ms"
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="invite")
    async def invite(self, ctx: KContext) -> None:
        """Invite Kumiko to your server!"""
        if self.bot.application_id is None:
            return None
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
        url = oauth_url(self.bot.application_id, permissions=perms)
        await ctx.send(url)

    @commands.is_owner()
    @commands.command(
        name="sys-metrics",
        aliases=["sysmetrics"],
        hidden=True,
    )
    async def sys_metrics(self, ctx: KContext) -> None:
        """Tells you the current system metrics along with other information"""
        await ctx.defer()
        mem = psutil.virtual_memory()
        proc = psutil.Process()
        with proc.oneshot():
            proc_mem = bytes2human(proc.memory_info().rss)
            disk_usage = psutil.disk_usage("/")
            embed = Embed()
            embed.title = "System Metrics + Info"
            embed.description = (
                f"**CPU:** {psutil.cpu_percent()}% (Proc - {proc.cpu_percent()}%)\n"
                f"**Mem:** {proc_mem} ({proc_mem}/{bytes2human(mem.total)})\n"
                f"**Disk (System):** {disk_usage.percent}% ({bytes2human(disk_usage.used)}/{bytes2human(disk_usage.total)})\n"
                f"**Proc Status:** {proc.status()}\n"
            )
            embed.add_field(name="Kernel Version", value=platform.release())
            embed.add_field(name="Python Compiler", value=platform.python_compiler())
            embed.add_field(
                name="Python Version", value=platform.python_version(), inline=True
            )
            embed.add_field(
                name="Discord.py Version", value=discord.__version__, inline=True
            )
            embed.add_field(name="Kumiko Build Version", value=str(self.bot.version))
            await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Meta(bot))
