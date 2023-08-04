from typing import Any, Dict

import asyncpg
import discord
from discord.ext import commands
from Libs.utils.pages import EmbedListSource, KumikoPages, SimplePageSource

from .modals import UserInvAHListModal, UserInvRefundModal


class BasePages(KumikoPages):
    def __init__(self, entries, *, ctx: commands.Context, per_page: int = 10):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(
            title="Leaderboard stats", colour=discord.Colour.from_rgb(219, 171, 255)
        )


class UserInvBasePages(KumikoPages):
    def __init__(
        self, entries, *, ctx: commands.Context, per_page: int = 1, pool: asyncpg.Pool
    ):
        super().__init__(
            EmbedListSource(entries, per_page=per_page), ctx=ctx, compact=True
        )
        self.pool = pool
        self.add_item(self.ah_list)
        self.add_item(self.refund)
        self.embed = discord.Embed(colour=discord.Colour.og_blurple())

    async def get_embed_from_page(self, current_page: int) -> Dict[str, Any]:
        page = await self.source.get_page(current_page)
        kwargs_from_page = await self.get_kwargs_from_page(page)
        return kwargs_from_page["embed"].to_dict()

    @discord.ui.button(
        custom_id="ah_list",
        emoji="<:auction_house:1136906394323398749>",
        label="List on Auction House",
        style=discord.ButtonStyle.grey,
        row=2,
    )
    async def ah_list(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """lists on AH"""
        page_data = await self.get_embed_from_page(self.current_page)
        item_id = int(page_data["fields"][0]["value"])
        curr_amount = int(page_data["fields"][-1]["value"])  # type: ignore
        await interaction.response.send_modal(
            UserInvAHListModal(curr_amount, item_id, self.pool)
        )

    @discord.ui.button(
        custom_id="refund_item",
        emoji=discord.PartialEmoji(name="\U0001f4b0"),
        label="Refund",
        style=discord.ButtonStyle.grey,
        row=2,
    )
    async def refund(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Basically refunds the item"""
        page_data = await self.get_embed_from_page(self.current_page)
        item_id = int(page_data["fields"][0]["value"])
        curr_amount = int(page_data["fields"][-1]["value"])  # type: ignore
        await interaction.response.send_modal(
            UserInvRefundModal(curr_amount, item_id, self.pool)
        )
