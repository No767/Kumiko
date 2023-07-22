import asyncpg
import discord
from attrs import asdict
from Libs.cache import KumikoCache
from Libs.cog_utils.events_log import disable_logging
from Libs.config import LoggingGuildConfig
from Libs.utils import ErrorEmbed, SuccessActionEmbed
from redis.asyncio.connection import ConnectionPool


class RegisterView(discord.ui.View):
    def __init__(self, pool: asyncpg.Pool, redis_pool: ConnectionPool) -> None:
        super().__init__()
        self.pool = pool
        self.redis_pool = redis_pool

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
            guildId = interaction.guild.id  # type: ignore
            cache = KumikoCache(connection_pool=self.redis_pool)
            lgc = LoggingGuildConfig(channel_id=select.values[0].id)
            tr = conn.transaction()
            await tr.start()

            try:
                await conn.execute(query, guildId, select.values[0].id, True)
            except asyncpg.UniqueViolationError:
                await tr.rollback()
                await interaction.response.send_message("There are duplicate records")
            except Exception:
                await tr.rollback()
                await interaction.response.send_message("Could not create records.")
            else:
                await tr.commit()
                await cache.setJSONCache(
                    key=f"cache:kumiko:{guildId}:guild_config",
                    value=asdict(lgc),
                    path=".logging_config",
                )
                await interaction.response.send_message(
                    f"Successfully set the logging channel to {select.values[0].mention}"
                )

    @discord.ui.button(label="Finish", style=discord.ButtonStyle.green)
    async def button_quit(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()


class UnregisterView(discord.ui.View):
    def __init__(self, pool: asyncpg.Pool, redis_pool: ConnectionPool) -> None:
        super().__init__()
        self.pool = pool
        self.redis_pool = redis_pool

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
            guildId = interaction.guild.id  # type: ignore

            tr = conn.transaction()
            await tr.start()

            try:
                await conn.execute(query, guildId, False)
            except asyncpg.UniqueViolationError:
                await tr.rollback()
                self.clear_items()
                uniqueViolationEmbed = ErrorEmbed(
                    description="There are duplicate records"
                )
                await interaction.response.edit_message(
                    embed=uniqueViolationEmbed, view=self
                )
            except Exception:
                await tr.rollback()
                self.clear_items()
                failedEmbed = ErrorEmbed(
                    description="Could not update or delete records"
                )
                await interaction.response.edit_message(embed=failedEmbed, view=self)
            else:
                await tr.commit()
                await disable_logging(guild_id=guildId, redis_pool=self.redis_pool)
                self.clear_items()
                successEmbed = SuccessActionEmbed()
                successEmbed.description = "Disabled and cleared all logging configs"

                await interaction.response.edit_message(embed=successEmbed, view=self)

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
