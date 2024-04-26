from discord import PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore
from libs.ui.events_log import RegisterView, UnregisterView
from libs.utils import ConfirmEmbed, Embed, is_manager


class EventsLog(commands.Cog):
    """Logging module to track joins, and economy events"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        self.events_name_list = ["member_events", "mod_events", "eco_events"]

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f4f0")

    @property
    def configurable(self) -> bool:
        return True

    @commands.hybrid_group(name="logs")
    async def logs(self, ctx: commands.Context) -> None:
        """Logs events and actions on your server"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @is_manager()
    @commands.guild_only()
    @logs.command(name="enable")
    async def enable(self, ctx: commands.Context) -> None:
        """Registers and enables events logging on the server"""
        register_info = "In order to get started, **only** select one of the options within the dropdown menu in order to set it.\nOnce you are done, click the finish button."
        embed = Embed(title="Registration Info")
        embed.description = register_info
        view = RegisterView(ctx=ctx, pool=self.pool, redis_pool=self.redis_pool)
        await ctx.send(embed=embed, view=view)

    @is_manager()
    @commands.guild_only()
    @logs.command(name="disable")
    async def disable(self, ctx: commands.Context) -> None:
        """Disables and unregisters the events logging on the server"""
        view = UnregisterView(ctx=ctx, pool=self.pool, redis_pool=self.redis_pool)
        embed = ConfirmEmbed()
        embed.description = "You are about to disable and unregister the events logging feature on Kumiko. Press Confirm to confirm your action."
        await ctx.send(embed=embed, view=view)

    @is_manager()
    @commands.guild_only()
    @logs.command(name="info")
    async def info(self, ctx: commands.Context) -> None:
        """Displays info about the events logging module"""
        results = {}
        embed = Embed()
        embed.set_author(name="Events Logging Info", icon_url=ctx.guild.icon.url)  # type: ignore
        embed.description = f"**Enabled?:** {results['logs']}\n**Events Logging Channel:** <#{results['logging_config']['channel_id']}>"
        embed.add_field(
            name="Member Events",
            value=f"Enabled?: **{results['logging_config']['member_events']}**",
        )
        embed.add_field(
            name="Mod Events",
            value=f"Enabled?: **{results['logging_config']['mod_events']}**",
        )
        embed.add_field(
            name="Eco Events",
            value=f"Enabled?: **{results['logging_config']['eco_events']}**",
        )
        await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsLog(bot))
