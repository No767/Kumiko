from discord import PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.ui.events_log import RegisterView, UnregisterView
from Libs.utils import ConfirmEmbed, Embed


class EventsLog(commands.Cog):
    """Logging module to track joins, and economy events"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U0001f4f0")

    @commands.hybrid_group(name="logs")
    async def logs(self, ctx: commands.Context) -> None:
        """Logs events and actions on your server"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @logs.command(name="enable")
    async def enableLogs(self, ctx: commands.Context) -> None:
        """Registers and enables events logging on the server"""
        registerInfo = "In order to get started, **only** select one of the options within the dropdown menu in order to set it.\nOnce you are done, click the finish button."
        embed = Embed(title="Registration Info")
        embed.description = registerInfo
        view = RegisterView(pool=self.pool)
        await ctx.send(embed=embed, view=view)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @logs.command(name="disable")
    async def disableLogs(self, ctx: commands.Context) -> None:
        """Disables and unregisters the events logging on the server"""
        view = UnregisterView(pool=self.pool)
        embed = ConfirmEmbed()
        embed.description = "You are about to disable and unregister the events logging feature on Kumiko. Press Confirm to confirm your action."
        await ctx.send(embed=embed, view=view)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @logs.command(name="info")
    async def logInfo(self, ctx: commands.Context) -> None:
        """Displays info about the events logging module"""
        query = """
        SELECT guild.id, guild.logs, logging_config.channel_id, logging_config.member_events, logging_config.mod_events, logging_config.eco_events
        FROM guild
        INNER JOIN logging_config
        ON guild.id = logging_config.guild_id
        WHERE guild.id = $1;
        """
        guild_id = ctx.guild.id  # type: ignore
        async with self.pool.acquire() as conn:
            result = await conn.fetchrow(query, guild_id)
            embed = Embed()
            embed.set_author(name="Events Logging Info", icon_url=ctx.guild.icon.url)  # type: ignore
            embed.description = f"**Enabled?:** {result['logs']}\n**Events Logging Channel:** <#{result['channel_id']}>"
            embed.add_field(
                name="Member Events", value=f"Enabled?: **{result['member_events']}**"
            )
            embed.add_field(
                name="Mod Events", value=f"Enabled?: **{result['mod_events']}**"
            )
            embed.add_field(
                name="Eco Events", value=f"Enabled?: **{result['eco_events']}**"
            )
            await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsLog(bot))
