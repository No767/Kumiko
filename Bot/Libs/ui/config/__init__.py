import asyncpg
import discord
from Libs.cog_utils.config import check_already_set, configure_settings
from Libs.utils import Embed, MessageConstants
from redis.asyncio.connection import ConnectionPool


class ConfigMenu(discord.ui.Select):
    def __init__(self, author_id: int, bot) -> None:
        self.author_id = author_id
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        options = [
            discord.SelectOption(
                emoji=getattr(cog, "display_emoji", None),
                label=cog_name,
                description=cog.__doc__.split("\n")[0]
                if cog.__doc__ is not None
                else None,
                value=cog_name,
            )
            for cog_name, cog in self.bot.cogs.items()
            if getattr(cog, "configurable", None) is not None
        ]
        super().__init__(placeholder="Select a category...", options=options, row=0)

    async def callback(self, interaction: discord.Interaction) -> None:
        # I know that this is pretty dirty on how to do it, but there is quite literally no other way to do it
        # You can't just define a variable for columns
        # See https://github.com/MagicStack/asyncpg/issues/208#issuecomment-335498184
        value = self.values[0]
        view = ConfirmToggleView(self.author_id, value, self.pool, self.redis_pool)
        embed = Embed()
        embed.description = "Select on the buttons below in order to enable or disable the current module."
        await interaction.response.send_message(embed=embed, view=view)


class ConfirmToggleView(discord.ui.View):
    def __init__(
        self, author_id: int, value: str, pool: asyncpg.Pool, redis_pool: ConnectionPool
    ):
        super().__init__()
        self.author_id = author_id
        self.value = value
        self.pool = pool
        self.redis_pool = redis_pool

    async def interaction_check(self, interaction: discord.Interaction, /):
        if interaction.user.id == self.author_id:
            return True
        await interaction.response.send_message(
            MessageConstants.NO_CONTROL_VIEW.value, ephemeral=True
        )
        return False

    @discord.ui.button(
        label="Enable",
        style=discord.ButtonStyle.green,
        emoji="<:greenTick:596576670815879169>",
        row=0,
    )
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        assert interaction.guild is not None
        if (
            await check_already_set(self.value, interaction.guild.id, self.redis_pool)
            is True
        ):
            await interaction.response.send_message(
                f"{self.value} is already enabled!", ephemeral=True
            )
            return
        # Must be disabled in order to run
        return_status = await configure_settings(
            status=True,
            value=self.value,
            guild_id=interaction.guild.id,
            pool=self.pool,
            redis_pool=self.redis_pool,
        )
        await interaction.response.send_message(return_status, ephemeral=True)

    @discord.ui.button(
        label="Disable",
        style=discord.ButtonStyle.red,
        emoji="<:redTick:596576672149667840>",
        row=0,
    )
    async def disable(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        assert interaction.guild is not None
        if (
            await check_already_set(self.value, interaction.guild.id, self.redis_pool)
            is False
        ):
            await interaction.response.send_message(
                f"{self.value} is already disabled!", ephemeral=True
            )
            return
        # Basically must be enabled in order to run
        return_status = await configure_settings(
            status=False,
            value=self.value,
            guild_id=interaction.guild.id,
            pool=self.pool,
            redis_pool=self.redis_pool,
        )
        await interaction.response.send_message(return_status, ephemeral=True)

    @discord.ui.button(
        label="Finish",
        style=discord.ButtonStyle.grey,
    )
    async def finish(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()


class ConfigMenuView(discord.ui.View):
    def __init__(self, author_id: int, bot) -> None:
        super().__init__()
        self.author_id = author_id
        self.add_item(ConfigMenu(author_id, bot))

    async def interaction_check(self, interaction: discord.Interaction, /):
        if interaction.user.id == self.author_id:
            return True
        await interaction.response.send_message(
            MessageConstants.NO_CONTROL_VIEW.value, ephemeral=True
        )
        return False

    @discord.ui.button(label="Finish", style=discord.ButtonStyle.green, row=1)
    async def finish(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await interaction.response.defer()
        await interaction.delete_original_response()
        self.stop()
