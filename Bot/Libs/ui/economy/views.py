import discord
from Libs.utils import Embed
from prisma.models import User


class RegisterView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        button.disabled = True
        doesUserExist = (
            await User.prisma().count(where={"id": interaction.user.id}, take=1) == 1
        )
        if doesUserExist:
            return await interaction.response.edit_message(
                embed=Embed(
                    title="Already Registered",
                    description="You already have an account!",
                ),
                view=self,
            )
        await User.prisma().create(
            data={"id": interaction.user.id, "name": interaction.user.name}
        )
        await interaction.edit_original_response(
            embed=Embed(
                title="Registered", description="You have successfully registered!"
            )
        )
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        button.disabled = True
        await interaction.response.edit_message(
            embed=Embed(title="Cancelled"), view=self
        )
        self.stop()
