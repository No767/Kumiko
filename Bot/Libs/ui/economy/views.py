import asyncpg
import discord
from discord.ext import commands
from Libs.utils import Embed, MessageConstants, SuccessEmbed


class RegisterView(discord.ui.View):
    def __init__(self, ctx: commands.Context, pool: asyncpg.Pool) -> None:
        super().__init__()
        self.ctx = ctx
        self.pool = pool

    async def interaction_check(self, interaction: discord.Interaction, /):
        if interaction.user.id == self.ctx.author.id:
            return True
        await interaction.response.send_message(
            MessageConstants.NO_CONTROL_VIEW.value, ephemeral=True
        )
        return False

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
            error_embed = Embed(description="You already have an economy account!")
            await interaction.response.edit_message(
                embed=error_embed, view=self, delete_after=20.0
            )
        else:
            success_embed = SuccessEmbed()
            success_embed.description = "Successfully created an economy account!"
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
