from __future__ import annotations

from typing import Optional

import discord


class NumberedPageModal(discord.ui.Modal, title="Go to page"):
    page = discord.ui.TextInput(
        label="Page", placeholder="Enter a number", min_length=1
    )

    def __init__(self, max_pages: Optional[int]) -> None:
        super().__init__()
        if max_pages is not None:
            as_string = str(max_pages)
            self.page.placeholder = f"Enter a number between 1 and {as_string}"
            self.page.max_length = len(as_string)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.interaction = interaction
        self.stop()
