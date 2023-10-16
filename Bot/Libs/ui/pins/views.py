import asyncpg
import discord
from discord.ext import commands
from Libs.utils import ErrorEmbed, MessageConstants, SuccessEmbed


class DeletePinView(discord.ui.View):
    def __init__(self, ctx: commands.Context, pool: asyncpg.Pool, name: str):
        super().__init__()
        self.author = ctx.author
        self.pool = pool
        self.name = name

    async def interaction_check(self, interaction: discord.Interaction, /):
        if interaction.user.id == self.author:
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
        DELETE FROM pin
        WHERE name = $1 OR $1 = ANY(aliases);
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, self.name)

            try:
                status = await conn.execute(query, self.name)
            except asyncpg.UniqueViolationError:
                self.clear_items()
                unique_violation_embed = ErrorEmbed(
                    description="There are duplicate records"
                )
                await interaction.response.edit_message(
                    embed=unique_violation_embed, view=self
                )
            else:
                self.clear_items()
                if status[-1] == "0":
                    error_embed = ErrorEmbed(
                        description=f"A pin with the name of `{self.name}` does not exist."
                    )
                    await interaction.response.edit_message(
                        embed=error_embed, view=self, delete_after=20.0
                    )
                else:
                    success_embed = SuccessEmbed()
                    success_embed.description = (
                        f"Deleted the following pin: `{self.name}`"
                    )
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


class PurgePinView(discord.ui.View):
    def __init__(self, ctx: commands.Context, pool: asyncpg.Pool):
        super().__init__()
        self.author = ctx.author
        self.pool = pool

    async def interaction_check(self, interaction: discord.Interaction, /):
        if interaction.user.id == self.author:
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
        DELETE FROM pin
        WHERE guild_id = $1 AND author_id=$2;
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                status = await conn.execute(query, interaction.guild.id, interaction.user.id)  # type: ignore
                self.clear_items()
                if status[-1] == "0":
                    error_embed = ErrorEmbed(
                        description="Either you don't own any pins or you have no permission to delete those pins"
                    )
                    await interaction.response.edit_message(
                        embed=error_embed, view=self, delete_after=20.0
                    )
                else:
                    success_embed = SuccessEmbed()
                    success_embed.description = (
                        f"Fully purged all pins belonging to {interaction.user.mention}"
                    )
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
