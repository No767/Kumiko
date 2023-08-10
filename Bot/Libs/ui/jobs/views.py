import asyncpg
import discord
from Libs.utils import ErrorEmbed, MessageConstants, SuccessActionEmbed


class DeleteJobView(discord.ui.View):
    def __init__(self, pool: asyncpg.pool.Pool, job_name: str) -> None:
        super().__init__()
        self.pool: asyncpg.pool.Pool = pool
        self.job_name = job_name

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        guild_id = interaction.guild.id  # type: ignore
        user_id = interaction.user.id
        query = """
        DELETE FROM job
        WHERE guild_id=$1 AND creator_id=$2 AND name= $3;
        """
        async with self.pool.acquire() as conn:
            status = await conn.execute(query, guild_id, user_id, self.job_name)
            self.clear_items()
            if status[-1] == "0":
                error_embed = ErrorEmbed(description=MessageConstants.NO_PERM_JOB.value)
                await interaction.response.edit_message(
                    embed=error_embed, view=self, delete_after=20.0
                )
            else:
                success_embed = SuccessActionEmbed()
                success_embed.description = f"Deleted job `{self.job_name}`"
                await interaction.response.edit_message(
                    embed=success_embed, view=self, delete_after=20.0
                )

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


class DeleteJobViaIDView(discord.ui.View):
    def __init__(self, pool: asyncpg.pool.Pool, job_id: int) -> None:
        super().__init__()
        self.pool: asyncpg.pool.Pool = pool
        self.job_id = job_id

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        guild_id = interaction.guild.id  # type: ignore
        user_id = interaction.user.id
        query = """
        DELETE FROM job
        WHERE guild_id=$1 AND creator_id=$2 AND id=$3;
        """
        async with self.pool.acquire() as conn:
            status = await conn.execute(query, guild_id, user_id, self.job_id)
            self.clear_items()
            if status[-1] == "0":
                error_embed = ErrorEmbed(description=MessageConstants.NO_PERM_JOB.value)
                await interaction.response.edit_message(
                    embed=error_embed, view=self, delete_after=20.0
                )
            else:
                success_embed = SuccessActionEmbed()
                success_embed.description = f"Deleted job via ID (ID: `{self.job_id}`)"
                await interaction.response.edit_message(
                    embed=success_embed, view=self, delete_after=20.0
                )

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


class PurgeJobsView(discord.ui.View):
    def __init__(self, pool: asyncpg.pool.Pool) -> None:
        super().__init__()
        self.pool: asyncpg.pool.Pool = pool

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        guild_id = interaction.guild.id  # type: ignore
        user_id = interaction.user.id
        query = """
        DELETE FROM job
        WHERE guild_id=$1 AND creator_id=$2;
        """
        async with self.pool.acquire() as conn:
            status = await conn.execute(query, guild_id, user_id)
            self.clear_items()
            if status[-1] == "0":
                error_embed = ErrorEmbed(description=MessageConstants.NO_PERM_JOB.value)
                await interaction.response.edit_message(
                    embed=error_embed, view=self, delete_after=20.0
                )
            else:
                success_embed = SuccessActionEmbed()
                success_embed.description = "Fully purged all jobs that you own."
                await interaction.response.edit_message(
                    embed=success_embed, view=self, delete_after=20.0
                )

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
