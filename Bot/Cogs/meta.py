import platform
from typing import Union

import discord
import psutil
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.meta import format_badges, format_date
from Libs.utils import Embed, human_timedelta
from psutil._common import bytes2human

TESTING_GUILD_ID = discord.Object(id=970159505390325842)
HANGOUT_GUILD_ID = discord.Object(id=1145897416160194590)


class Meta(commands.Cog):
    """Commands to obtain info about Kumiko or others"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U00002754")

    def get_bot_uptime(self, *, brief: bool = False) -> str:
        return human_timedelta(
            self.bot.uptime, accuracy=None, brief=brief, suffix=False
        )

    @commands.hybrid_command(name="uptime")
    async def uptime(self, ctx: commands.Context) -> None:
        """Returns uptime for Kumiko"""
        embed = Embed()
        embed.description = f"Kumiko's Uptime: **{self.get_bot_uptime()}**"
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

        desc = f"{format_badges(ctx, user)}"

        desc = f"""
        {format_badges(ctx, user)}
        
        **Name/ID**: {user.global_name} / {user.id}
        **Created**: {format_date(user.created_at)}
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
    async def about(self, ctx: commands.Context) -> None:
        """Shows some basic info about Kumiko"""
        embed = Embed()
        embed.title = f"{self.bot.user.name} Info"  # type: ignore
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)  # type: ignore
        embed.add_field(name="Server Count", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="User Count", value=len(self.bot.users), inline=True)
        embed.add_field(
            name="Python Version", value=platform.python_version(), inline=True
        )
        embed.add_field(
            name="Discord.py Version", value=discord.__version__, inline=True
        )
        embed.add_field(
            name="Kumiko Build Version", value=str(self.bot.version), inline=True
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="version")
    async def version(self, ctx: commands.Context) -> None:
        """Returns the current version of Kumiko"""
        embed = Embed()
        embed.description = f"Build Version: {str(self.bot.version)}"
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """Returns the current latency of Kumiko"""
        embed = Embed()
        embed.description = f"Pong! {round(self.bot.latency * 1000)}ms"
        await ctx.send(embed=embed)

    @commands.is_owner()
    @app_commands.guilds(TESTING_GUILD_ID, HANGOUT_GUILD_ID)
    @commands.hybrid_command(name="sys-metrics", aliases=["sysmetrics"])
    async def sys_metrics(self, ctx: commands.Context) -> None:
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
