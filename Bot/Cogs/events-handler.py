from typing import Mapping

import asyncpg
import discord
from attrs import asdict
from discord.ext import commands
from discord.utils import format_dt, utcnow
from kumikocore import KumikoCore
from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import get_or_fetch_config, get_or_fetch_log_enabled
from Libs.config import GuildConfig, LoggingGuildConfig
from Libs.utils import CancelledActionEmbed, Embed, SuccessActionEmbed
from redis.asyncio.connection import ConnectionPool


class EventsHandler(commands.Cog):
    """Cog for handling discord api events"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool

    async def ensureAllEnabled(
        self,
        guild_id: int,
        pool: asyncpg.Pool,
        redis_pool: ConnectionPool,
        logging_config: Mapping[str, bool],
        event: str,
    ) -> bool:
        logsEnabled = await get_or_fetch_log_enabled(guild_id, redis_pool, pool)
        return logsEnabled is True and logging_config[event] is True

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        existsQuery = "SELECT EXISTS(SELECT 1 FROM guild WHERE id = $1);"
        insertQuery = """
        WITH guild_insert AS (
            INSERT INTO guild (id) VALUES ($1)
        )
        INSERT INTO logging_config (guild_id) VALUES ($1);
        """
        cache = KumikoCache(connection_pool=self.redis_pool)
        key = f"cache:kumiko:{guild.id}:guild_config"
        guildConfig = GuildConfig(
            id=guild.id, logging_config=LoggingGuildConfig(channel_id=None)
        )
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                exists = await conn.fetchval(existsQuery, guild.id)
                if exists is False:
                    await conn.execute(insertQuery, guild.id)
                    await cache.setJSONCache(
                        key=key,
                        value=asdict(guildConfig, recurse=True),
                        path="$",
                        ttl=None,
                    )
                    self.bot.prefixes[guild.id] = None

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        cache = KumikoCache(connection_pool=self.redis_pool)
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("DELETE FROM guild WHERE id = $1", guild.id)
                del self.bot.prefixes[guild.id]
                await cache.deleteJSONCache(
                    key=f"cache:kumiko:{guild.id}:guild_config", path="$"
                )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        guild = member.guild
        getConfig = await get_or_fetch_config(
            id=member.guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if await self.ensureAllEnabled(guild.id, self.pool, self.redis_pool, getConfig, "member_events"):  # type: ignore
            channel = guild.get_channel(getConfig["channel_id"])  # type: ignore
            if isinstance(channel, discord.TextChannel):
                embed = SuccessActionEmbed()
                embed.title = "Member Joined"
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.description = f"{member.mention} {member.global_name}"
                embed.timestamp = utcnow()
                embed.add_field(
                    name="Account Age", value=format_dt(member.created_at, "R")
                )
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        guild = member.guild
        getConfig = await get_or_fetch_config(
            id=guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if await self.ensureAllEnabled(guild.id, self.pool, self.redis_pool, getConfig, "member_events"):  # type: ignore
            channel = guild.get_channel(getConfig["channel_id"])  # type: ignore
            if isinstance(channel, discord.TextChannel):
                embed = CancelledActionEmbed()
                embed.title = "Member Left"
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.description = f"{member.mention} {member.global_name}"
                embed.timestamp = utcnow()
                embed.add_field(
                    name="Account Age", value=format_dt(member.created_at, "R")
                )
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User) -> None:
        getConfig = await get_or_fetch_config(
            id=guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if await self.ensureAllEnabled(guild.id, self.pool, self.redis_pool, getConfig, "member_events"):  # type: ignore
            channel = guild.get_channel(getConfig["channel_id"])  # type: ignore
            if isinstance(channel, discord.TextChannel):
                embed = CancelledActionEmbed()
                embed.title = "Member Banned"
                embed.set_thumbnail(url=user.display_avatar.url)
                embed.description = f"{user.mention} {user.global_name}"
                embed.timestamp = utcnow()
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User) -> None:
        getConfig = await get_or_fetch_config(
            id=guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if await self.ensureAllEnabled(guild.id, self.pool, self.redis_pool, getConfig, "member_events"):  # type: ignore
            channel = guild.get_channel(getConfig["channel_id"])  # type: ignore
            if isinstance(channel, discord.TextChannel):
                embed = Embed(color=discord.Color.from_rgb(255, 143, 143))
                embed.title = "Member Unbanned"
                embed.set_thumbnail(url=user.display_avatar.url)
                embed.description = f"{user.mention} {user.global_name}"
                embed.timestamp = utcnow()
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_kick(self, guild: discord.Guild, user: discord.User) -> None:
        getConfig = await get_or_fetch_config(
            id=guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if await self.ensureAllEnabled(guild.id, self.pool, self.redis_pool, getConfig, "member_events"):  # type: ignore
            channel = guild.get_channel(getConfig["channel_id"])  # type: ignore
            if isinstance(channel, discord.TextChannel):
                embed = CancelledActionEmbed()
                embed.title = "Member Kicked"
                embed.set_thumbnail(url=user.display_avatar.url)
                embed.description = f"{user.mention} {user.global_name}"
                embed.timestamp = utcnow()
                await channel.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(EventsHandler(bot))
