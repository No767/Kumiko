from typing import Optional

import asyncpg
import discord
from Libs.cog_utils.economy import refund_item


class UserInvAHListModal(discord.ui.Modal, title="Send"):
    amount = discord.ui.TextInput(
        label="Amount", placeholder="Enter a number", min_length=1
    )

    def __init__(self, max_amount: Optional[int], item_id: int, pool: asyncpg.Pool):
        super().__init__()
        self.item_id = item_id
        self.pool = pool
        if max_amount is not None:
            as_str = str(max_amount)
            self.amount.placeholder = f"Enter a number between 1 and {as_str}"
            self.amount.max_length = len(as_str)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("nice")


class UserInvRefundModal(discord.ui.Modal, title="Refund an item"):
    amount = discord.ui.TextInput(
        label="Amount", placeholder="Enter a number", min_length=1
    )

    def __init__(self, max_amount: Optional[int], item_id: int, pool: asyncpg.Pool):
        super().__init__()
        self.item_id = item_id
        self.pool = pool
        if max_amount is not None:
            as_str = str(max_amount)
            self.amount.placeholder = f"Enter a number between 1 and {as_str}"
            self.amount.max_length = len(as_str)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if interaction.guild is None:
            await interaction.response.send_message(
                "You need to be in a server in order for this to work", ephemeral=True
            )
            return
        item_refund = await refund_item(
            interaction.guild.id,
            interaction.user.id,
            self.item_id,
            int(self.amount.value),
            self.pool,
        )
        await interaction.response.send_message(item_refund, ephemeral=True)
