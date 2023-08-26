from discord import PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import EventsFlag, get_or_fetch_channel_id
from Libs.config import LoggingGuildConfig, get_or_fetch_guild_config
from Libs.ui.events_log import RegisterView, UnregisterView
from Libs.utils import ConfirmEmbed, Embed, is_manager


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
        view = RegisterView(pool=self.pool, redis_pool=self.redis_pool)
        await ctx.send(embed=embed, view=view)

    @is_manager()
    @commands.guild_only()
    @logs.command(name="disable")
    async def disable(self, ctx: commands.Context) -> None:
        """Disables and unregisters the events logging on the server"""
        view = UnregisterView(pool=self.pool, redis_pool=self.redis_pool)
        embed = ConfirmEmbed()
        embed.description = "You are about to disable and unregister the events logging feature on Kumiko. Press Confirm to confirm your action."
        await ctx.send(embed=embed, view=view)

    @is_manager()
    @commands.guild_only()
    @logs.command(name="info")
    async def info(self, ctx: commands.Context) -> None:
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

    @is_manager()
    @commands.guild_only()
    @logs.command(name="configure", aliases=["config"], usage="all: bool")
    async def config(
        self, ctx: commands.Context, name: str, status: bool, *, events: EventsFlag
    ) -> None:
        """Configures which events are enabled. Using the all flag enabled all events."""
        if name not in self.events_name_list:
            await ctx.send(
                "The name of the event was not found. The possible events are:\nmember_events\nmod_events\neco_events"
            )
            return
        query = """
        UPDATE logging_config
        SET member_events = $2, mod_events = $3, eco_events = $4
        WHERE guild_id = $1;
        """
        guild_id = ctx.guild.id  # type: ignore
        key = f"cache:kumiko:{guild_id}:guild_config"
        cache = KumikoCache(connection_pool=self.redis_pool)
        get_channel_id = await get_or_fetch_channel_id(
            guild_id=guild_id, pool=self.pool, redis_pool=self.redis_pool
        )
        if get_channel_id is None:
            await ctx.send("The config was not set up. Please enable the logs module")
            return

        statuses = {
            "member_events": status if name in "member_events" else False,
            "mod_events": status if name in "mod_events" else False,
            "eco_events": status if name in "eco_events" else False,
        }

        lgc = LoggingGuildConfig(
            channel_id=int(get_channel_id),
            member_events=statuses["member_events"],
            mod_events=statuses["mod_events"],
            eco_events=statuses["eco_events"],
        )
        if events.all is True:
            lgc = LoggingGuildConfig(
                channel_id=int(get_channel_id),
                member_events=True,
                mod_events=True,
                eco_events=True,
            )
            await self.pool.execute(query, guild_id, True, True, True)
        else:
            await self.pool.execute(
                query,
                guild_id,
                statuses["member_events"],
                statuses["mod_events"],
                statuses["eco_events"],
            )

        await cache.merge_json_cache(
            key=key, value=lgc, path=".logging_config", ttl=None
        )
        await ctx.send("Updated successfully!")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsLog(bot))
