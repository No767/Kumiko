from typing import Union

import discord
from Libs.cog_utils.redirects import mark_as_resolved


class ConfirmResolvedView(discord.ui.View):
    def __init__(
        self,
        thread: discord.Thread,
        author: Union[discord.User, discord.Member],
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.thread = thread
        self.author = author

    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "You are not the author of the thread", ephemeral=True
            )
            return

        # Avoid relocking locked threads
        if self.thread.locked:
            return

        await interaction.response.send_message(
            "Marking this as solved. Next time you can mark it resolved yourself by using the command `>resolved`"
        )
        assert interaction.message is not None
        await interaction.message.add_reaction(discord.PartialEmoji(name="\U00002705"))
        await mark_as_resolved(self.thread, self.author)

    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
    )
    async def cancel(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.delete_original_response()
        self.stop()
