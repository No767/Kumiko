from typing import Mapping, Union

import asyncpg
import discord
from discord.ext import commands
from discord.utils import format_dt, utcnow
from kumikocore import KumikoCore
from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import (
    get_or_fetch_config,
    get_or_fetch_log_enabled,
)
from Libs.config import GuildConfig, LoggingGuildConfig
from Libs.utils import Embed, SuccessEmbed
from redis.asyncio.connection import ConnectionPool


class EventsHandler(commands.Cog):
    """Cog for handling discord api events"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool

    async def ensure_all_enabled(
        self,
        guild_id: int,
        pool: asyncpg.Pool,
        redis_pool: ConnectionPool,
        logging_config: Mapping[str, bool],
        event: str,
    ) -> bool:
        logs_enabled = await get_or_fetch_log_enabled(guild_id, redis_pool, pool)
        return logs_enabled is True and logging_config[event] is True

    def produce_embeds(
        self,
        member: Union[discord.Member, discord.User],
        type: str,
        type_msg: str,
        display_age: bool = True,
    ) -> discord.Embed:
        embed = SuccessEmbed(title=type_msg)

        if type == "unban":
            embed = Embed(color=discord.Color.from_rgb(255, 143, 143))
        elif type == "kick":
            embed = Embed(color=discord.Color.blurple())
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.description = f"{member.mention} {member.global_name}"
        embed.timestamp = utcnow()
        embed.set_footer(text="Happened At")
        if display_age:
            embed.add_field(name="Account Age", value=format_dt(member.created_at, "R"))
            embed.add_field(name="Joined At", value=format_dt(member.joined_at or utcnow()))  # type: ignore
        return embed

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        exists_query = "SELECT EXISTS(SELECT 1 FROM guild WHERE id = $1);"
        insert_query = """
        WITH guild_insert AS (
            INSERT INTO guild (id) VALUES ($1)
        )
        INSERT INTO logging_config (guild_id) VALUES ($1);
        """
        cache = KumikoCache(connection_pool=self.redis_pool)
        key = f"cache:kumiko:{guild.id}:guild_config"
        guild_config = GuildConfig(
            id=guild.id, logging_config=LoggingGuildConfig(channel_id=None)
        )
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                exists = await conn.fetchval(exists_query, guild.id)
                if exists is False:
                    await conn.execute(insert_query, guild.id)
                    await cache.set_json_cache(
                        key=key,
                        value=guild_config,
                        path="$",
                        ttl=None,
                    )
                    self.bot.prefixes[guild.id] = None

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        cache = KumikoCache(connection_pool=self.redis_pool)
        await self.pool.execute("DELETE FROM guild WHERE id = $1", guild.id)
        await cache.delete_json_cache(
            key=f"cache:kumiko:{guild.id}:guild_config", path="$"
        )
        if guild.id in self.bot.prefixes:
            del self.bot.prefixes[guild.id]

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User) -> None:
        get_config = await get_or_fetch_config(
            id=guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if await self.ensure_all_enabled(guild.id, self.pool, self.redis_pool, get_config, "mod_events"):  # type: ignore
            channel = guild.get_channel(get_config["channel_id"])  # type: ignore
            if isinstance(channel, discord.TextChannel):
                embed = self.produce_embeds(
                    member=user,
                    type="leave",
                    type_msg="Member Banned",
                )
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User) -> None:
        get_config = await get_or_fetch_config(
            id=guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if await self.ensure_all_enabled(guild.id, self.pool, self.redis_pool, get_config, "mod_events"):  # type: ignore
            channel = guild.get_channel(get_config["channel_id"])  # type: ignore
            if isinstance(channel, discord.TextChannel):
                embed = self.produce_embeds(
                    member=user,
                    type="unban",
                    type_msg="Member Unbanned",
                )
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_kick(self, guild: discord.Guild, user: discord.User) -> None:
        get_config = await get_or_fetch_config(
            id=guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if await self.ensure_all_enabled(guild.id, self.pool, self.redis_pool, get_config, "mod_events"):  # type: ignore
            channel = guild.get_channel(get_config["channel_id"])  # type: ignore
            if isinstance(channel, discord.TextChannel):
                embed = self.produce_embeds(
                    member=user,
                    type="leave",
                    type_msg="Member Kicked",
                )
                await channel.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsHandler(bot))
