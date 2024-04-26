from typing import TYPE_CHECKING

import asyncpg
import discord
from libs.cog_utils.pride_profiles import snake_case_to_title
from libs.utils import KumikoModal

if TYPE_CHECKING:
    from libs.utils.context import KContext


class EditProfileModal(KumikoModal, title="Edit Profile"):
    def __init__(self, ctx: KContext, profile_type: str, pool: asyncpg.Pool) -> None:
        super().__init__(ctx)
        self.pool = pool
        self.profile_type = profile_type
        self.cleaned_type = snake_case_to_title(profile_type)
        self.profile_category = discord.ui.TextInput(
            label=f"Change your {self.cleaned_type} status",
            placeholder=f"Enter your new {self.cleaned_type} status",
            min_length=1,
            max_length=50,
        )
        self.add_item(self.profile_category)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # https://github.com/MagicStack/asyncpg/issues/208
        # Because of this, we are going to use it the good old fashioned way
        # not the best lol
        query = """
        UPDATE pride_profiles
        SET name = $2
        WHERE id = $1;
        """
        if self.profile_type in "pronouns":
            query = """
            UPDATE pride_profiles
            SET pronouns = $2
            WHERE id = $1;
            """
        elif self.profile_type in "gender_identity":
            query = """
            UPDATE pride_profiles
            SET gender_identity = $2
            WHERE id = $1;
            """
        elif self.profile_type in "sexual_orientation":
            query = """
            UPDATE pride_profiles
            SET sexual_orientation = $2
            WHERE id = $1;
            """
        elif self.profile_type in "romantic_orientation":
            query = """
            UPDATE pride_profiles
            SET romantic_orientation = $2
            WHERE id = $1;
            """
        await self.pool.execute(query, interaction.user.id, self.profile_category.value)
        await interaction.response.send_message(
            f'Changed your "{self.cleaned_type}" status to "{self.profile_category.value}"',
            ephemeral=True,
        )
