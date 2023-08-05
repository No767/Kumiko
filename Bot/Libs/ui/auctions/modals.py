from typing import Optional

import asyncpg
import discord
from Libs.cog_utils.auctions import add_more_to_auction


class OwnedAuctionItemAdd(discord.ui.Modal, title="Add more"):
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
                "You can't use this feature in DMs", ephemeral=True
            )
            return

        status = await add_more_to_auction(
            guild_id=interaction.guild.id,
            user_id=interaction.user.id,
            pool=self.pool,
            item_id=self.item_id,
            amount_requested=int(self.amount.value),
        )
        await interaction.response.send_message(status, ephemeral=True)
        return
