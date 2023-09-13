import asyncpg
import discord
from discord.ext import commands
from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import disable_logging
from Libs.config import LoggingGuildConfig
from Libs.utils import ErrorEmbed, MessageConstants, SuccessActionEmbed
from redis.asyncio.connection import ConnectionPool


class RegisterView(discord.ui.View):
    def __init__(
        self, ctx: commands.Context, pool: asyncpg.Pool, redis_pool: ConnectionPool
    ) -> None:
        super().__init__()
        self.ctx = ctx
        self.pool = pool
        self.redis_pool = redis_pool

    async def interaction_check(self, interaction: discord.Interaction, /):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message(
            MessageConstants.NO_CONTROL_VIEW.value, ephemeral=True
        )
        return False

    @discord.ui.select(
        cls=discord.ui.ChannelSelect, channel_types=[discord.ChannelType.text]
    )
    async def select_channels(
        self, interaction: discord.Interaction, select: discord.ui.ChannelSelect
    ) -> None:
        query = """
        WITH guild_update AS (
            UPDATE guild
            SET logs = $3
            WHERE id = $1
            RETURNING id
        )
        INSERT INTO logging_config (channel_id, guild_id)
        VALUES ($2, (SELECT id FROM guild_update))
        ON CONFLICT (guild_id) DO 
        UPDATE SET channel_id = excluded.channel_id;
        """
        async with self.pool.acquire() as conn:
            guild_id = interaction.guild.id  # type: ignore
            cache = KumikoCache(connection_pool=self.redis_pool)
            lgc = LoggingGuildConfig(channel_id=select.values[0].id)
            tr = conn.transaction()
            await tr.start()

            try:
                await conn.execute(query, guild_id, select.values[0].id, True)
            except asyncpg.UniqueViolationError:
                await tr.rollback()
                await interaction.response.send_message("There are duplicate records")
            except Exception:
                await tr.rollback()
                await interaction.response.send_message("Could not create records.")
            else:
                await tr.commit()
                await cache.merge_json_cache(
                    key=f"cache:kumiko:{guild_id}:guild_config",
                    value=lgc,
                    path=".logging_config",
                )
                await cache.set_basic_cache(
                    key=f"cache:kumiko:{guild_id}:logging_channel_id",
                    value=str(select.values[0].id),
                    ttl=3600,
                )
                await interaction.response.send_message(
                    f"Successfully set the logging channel to {select.values[0].mention}",
                    ephemeral=True,
                )

    @discord.ui.button(label="Finish", style=discord.ButtonStyle.green)
    async def button_quit(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()


class UnregisterView(discord.ui.View):
    def __init__(
        self, ctx: commands.Context, pool: asyncpg.Pool, redis_pool: ConnectionPool
    ) -> None:
        super().__init__()
        self.ctx = ctx
        self.pool = pool
        self.redis_pool = redis_pool

    async def interaction_check(self, interaction: discord.Interaction, /):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message(
            MessageConstants.NO_CONTROL_VIEW.value, ephemeral=True
        )
        return False

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        query = """
        WITH guild_update AS (
            UPDATE guild
            SET logs = $2
            WHERE id = $1
            RETURNING id
        )
        DELETE FROM logging_config WHERE guild_id = (SELECT id FROM guild_update);
        """
        async with self.pool.acquire() as conn:
            guild_id = interaction.guild.id  # type: ignore

            tr = conn.transaction()
            await tr.start()

            try:
                await conn.execute(query, guild_id, False)
            except asyncpg.UniqueViolationError:
                await tr.rollback()
                self.clear_items()
                unique_violation_embed = ErrorEmbed(
                    description="There are duplicate records"
                )
                await interaction.response.edit_message(
                    embed=unique_violation_embed, view=self
                )
            except Exception:
                await tr.rollback()
                self.clear_items()
                failed_embed = ErrorEmbed(
                    description="Could not update or delete records"
                )
                await interaction.response.edit_message(embed=failed_embed, view=self)
            else:
                await tr.commit()
                await disable_logging(guild_id=guild_id, redis_pool=self.redis_pool)
                self.clear_items()
                success_embed = SuccessActionEmbed()
                success_embed.description = "Disabled and cleared all logging configs"

                await interaction.response.edit_message(embed=success_embed, view=self)

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
    )
    async def cancel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()
