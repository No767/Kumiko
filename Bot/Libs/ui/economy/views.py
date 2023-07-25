import asyncpg
import discord
from Libs.utils import Embed, SuccessActionEmbed


class RegisterView(discord.ui.View):
    def __init__(self, pool: asyncpg.Pool) -> None:
        super().__init__()
        self.pool = pool

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        query = """
        INSERT INTO eco_user (id)
        VALUES ($1);
        """
        status = await self.pool.execute(query, interaction.user.id)
        self.clear_items()
        if status[-1] == "0":
            errorEmbed = Embed(description="You already have an economy account!")
            await interaction.response.edit_message(
                embed=errorEmbed, view=self, delete_after=20.0
            )
        else:
            successEmbed = SuccessActionEmbed()
            successEmbed.description = "Successfully created an economy account!"
            await interaction.response.edit_message(
                embed=successEmbed, view=self, delete_after=20.0
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
