import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import EventsFlag, get_or_fetch_channel_id
from Libs.config import LoggingGuildConfig
from Libs.ui.config import ConfigMenuView
from Libs.utils import Embed, is_manager


class Config(commands.Cog):
    """Custom configuration layer for Kumiko"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        self.events_name_list = ["member_events", "mod_events", "eco_events"]

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    @is_manager()
    @commands.hybrid_group(name="configure", aliases=["config"], fallback="features")
    async def config(self, ctx: commands.Context) -> None:
        """Configure the settings for Kumiko"""
        view = ConfigMenuView(self.bot, ctx)
        embed = Embed()
        embed.description = "If you are the owner or a server mod, this is the main configuration menu! This menu is meant for enabling/disabling features."
        embed.add_field(
            name="How to use",
            value="Click on the select menu, and enable/disable the selected feature. Once finished, just click the 'Finish' button",
            inline=False,
        )
        embed.set_author(name="Kumiko's Configuration Menu", icon_url=self.bot.user.display_avatar.url)  # type: ignore
        await ctx.send(embed=embed, view=view)

    @is_manager()
    @config.command(name="logs", usage="all: bool")
    async def configure_logs(
        self, ctx: commands.Context, name: str, status: bool, *, events: EventsFlag
    ) -> None:
        """Configures which events for logging are enabled. Using the all flag enabled all events."""
        assert ctx.guild is not None
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
        guild_id = ctx.guild.id
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
            mod_events=statuses["mod_events"],
            eco_events=statuses["eco_events"],
        )
        if events.all is True:
            lgc = LoggingGuildConfig(
                channel_id=int(get_channel_id),
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
    await bot.add_cog(Config(bot))
