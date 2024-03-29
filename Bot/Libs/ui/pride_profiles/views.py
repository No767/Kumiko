import asyncpg
import discord
from discord.ext import commands
from Libs.utils import ErrorEmbed, KumikoView, SuccessEmbed

from .selects import SelectPrideCategory


class ConfirmRegisterView(KumikoView):
    def __init__(self, ctx: commands.Context, pool: asyncpg.Pool) -> None:
        super().__init__(ctx)
        self.pool = pool

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:

        query = """
        INSERT INTO pride_profiles (id, name)
        VALUES ($1, $2)
        ON CONFLICT (id) DO NOTHING;
        """
        status = await self.pool.execute(
            query, interaction.user.id, interaction.user.global_name
        )

        if status[-1] != "0":
            success_embed = SuccessEmbed()
            success_embed.description = "Registered your pride profile!"
            await interaction.response.edit_message(
                embed=success_embed, delete_after=10.0, view=None
            )
        else:
            error_embed = ErrorEmbed(title="Already registered")
            error_embed.description = "You already have a pride profile registered!"
            await interaction.response.edit_message(
                embed=error_embed, delete_after=10.0, view=None
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


class ConfigureView(KumikoView):
    def __init__(self, ctx: commands.Context, pool: asyncpg.Pool) -> None:
        super().__init__(ctx)
        self.add_item(SelectPrideCategory(ctx, pool))

    @discord.ui.button(label="Finish", style=discord.ButtonStyle.green, row=1)
    async def finish(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()


class DeleteProfileView(KumikoView):
    def __init__(self, ctx: commands.Context, pool: asyncpg.Pool) -> None:
        super().__init__(ctx)
        self.pool = pool

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:

        query = """
        DELETE FROM pride_profiles
        WHERE id = $1;
        """
        status = await self.pool.execute(query, interaction.user.id)

        if status[-1] != "0":
            success_embed = SuccessEmbed()
            success_embed.description = "Successfully deleted your pride profile"
            await interaction.response.edit_message(
                embed=success_embed, delete_after=10.0, view=None
            )
        else:
            error_embed = ErrorEmbed(title="Doesn't exist")
            error_embed.description = (
                "The pride profile that you are trying to delete doesn't exist"
            )
            await interaction.response.edit_message(
                embed=error_embed, delete_after=10.0, view=None
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
