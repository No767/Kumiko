from attrs import asdict
from discord import PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import EventsFlag, get_or_fetch_config
from Libs.config import LoggingGuildConfig, get_or_fetch_guild_config
from Libs.ui.events_log import RegisterView, UnregisterView
from Libs.utils import ConfirmEmbed, Embed


class EventsLog(commands.Cog):
    """Logging module to track joins, and economy events"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool

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
        view = RegisterView(pool=self.pool, redis_pool=self.redis_pool)
        await ctx.send(embed=embed, view=view)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @logs.command(name="disable")
    async def disableLogs(self, ctx: commands.Context) -> None:
        """Disables and unregisters the events logging on the server"""
        view = UnregisterView(pool=self.pool, redis_pool=self.redis_pool)
        embed = ConfirmEmbed()
        embed.description = "You are about to disable and unregister the events logging feature on Kumiko. Press Confirm to confirm your action."
        await ctx.send(embed=embed, view=view)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @logs.command(name="info")
    async def logInfo(self, ctx: commands.Context) -> None:
        """Displays info about the events logging module"""
        guild_id = ctx.guild.id  # type: ignore
        results = await get_or_fetch_guild_config(guild_id, self.pool, self.redis_pool)
        if results is None:
            await ctx.send("The config was not set up. Please enable the logs module")
            return
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

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @logs.command(name="configure", aliases=["config"])
    async def logConfig(self, ctx: commands.Context, events: EventsFlag) -> None:
        """Configures which events are enabled"""
        query = """
        UPDATE logging_config
        SET member_events = $2, mod_events = $3, eco_events = $4
        WHERE guild_id = $1;
        """
        guild_id = ctx.guild.id  # type: ignore
        key = f"cache:kumiko:{guild_id}:guild_config"
        cache = KumikoCache(connection_pool=self.redis_pool)
        getConfig = await get_or_fetch_config(
            id=guild_id, redis_pool=self.redis_pool, pool=self.pool
        )
        if getConfig is None:
            await ctx.send("The config was not set up. Please enable the logs module")
            return

        lgc = LoggingGuildConfig(
            channel_id=getConfig["channel_id"],
            member_events=events.member,
            mod_events=events.mod,
            eco_events=events.eco,
        )
        if events.all is True:
            lgc = LoggingGuildConfig(
                channel_id=getConfig["channel_id"],
                member_events=True,
                mod_events=True,
                eco_events=True,
            )

        await self.pool.execute(query, guild_id, events.member, events.mod, events.eco)
        await cache.setJSONCache(key=key, value=asdict(lgc), path=".logging_config")
        await ctx.send("Updated successfully!")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsLog(bot))
