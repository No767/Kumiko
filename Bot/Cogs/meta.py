import platform

import discord
import psutil
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
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
    async def info(self, ctx: commands.Context) -> None:
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
