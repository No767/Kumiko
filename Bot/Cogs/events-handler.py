from typing import Any

import discord
from discord.ext import commands
from discord.utils import format_dt, utcnow
from kumikocore import KumikoCore
from Libs.cog_utils.events_log import get_or_fetch_config
from Libs.utils import CancelledActionEmbed, Embed, SuccessActionEmbed


class EventsHandler(commands.Cog):
    """Cog for handling discord api events"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool

    def ensureEnabled(self, config: Any) -> bool:
        if (config is not None) and (
            config["logs"] and config["member_events"] is True
        ):
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        existsQuery = "SELECT EXISTS(SELECT 1 FROM guild WHERE id = $1);"
        insertQuery = """
        INSERT INTO guild (id) VALUES ($1);
        INSERT INTO logging_config (guild_id) VALUES ($1);
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                exists = await conn.fetchval(existsQuery, guild.id)
                if not exists:
                    await conn.execute(insertQuery, guild.id)
                    self.bot.prefixes[guild.id] = [self.bot.default_prefix]

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("DELETE FROM guild WHERE id = $1", guild.id)
                self.bot.prefixes[guild.id] = self.bot.default_prefix

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        guild = member.guild
        getConfig = await get_or_fetch_config(
            id=member.guild.id, redis_pool=self.redis_pool, pool=self.pool
        )
        if self.ensureEnabled(getConfig):
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
        if self.ensureEnabled(getConfig):
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
        if self.ensureEnabled(getConfig):
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
        if self.ensureEnabled(getConfig):
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
        if self.ensureEnabled(getConfig):
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
