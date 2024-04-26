from typing import Any, Dict

import asyncpg
import discord
from discord.ext import commands
from libs.cog_utils.auctions import delete_auction
from libs.utils.pages import EmbedListSource, KumikoPages, SimplePageSource

from .modals import OwnedAuctionItemAdd


class OwnedAuctionItemBasePages(KumikoPages):
    def __init__(
        self, entries, *, ctx: commands.Context, pool: asyncpg.Pool, per_page: int = 1
    ):
        super().__init__(
            EmbedListSource(entries, per_page=per_page), ctx=ctx, compact=True
        )
        self.add_item(self.add_more)
        self.add_item(self.delete)
        self.embed = discord.Embed(colour=discord.Colour.og_blurple())
        self.ctx = ctx
        self.pool = pool

    async def get_embed_from_page(self, current_page: int) -> Dict[str, Any]:
        page = await self.source.get_page(current_page)
        kwargs_from_page = await self.get_kwargs_from_page(page)
        return kwargs_from_page["embed"].to_dict()

    @discord.ui.button(
        custom_id="add_more", label="Add More", style=discord.ButtonStyle.grey, row=2
    )
    async def add_more(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """add more"""
        page_data = await self.get_embed_from_page(self.current_page)
        item_id = int(page_data["fields"][-1]["value"])
        curr_amount = int(page_data["fields"][3]["value"])
        await interaction.response.send_modal(
            OwnedAuctionItemAdd(self.ctx, curr_amount, item_id, self.pool)
        )

    @discord.ui.button(
        custom_id="delete", label="Delete", style=discord.ButtonStyle.grey, row=2
    )
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        page_data = await self.get_embed_from_page(self.current_page)
        item_id = int(page_data["fields"][-1]["value"])

        if interaction.guild is None:
            await interaction.response.send_message(
                "You need to be in a server in order for this to work", ephemeral=True
            )
            return
        status = await delete_auction(
            guild_id=interaction.guild.id,
            user_id=interaction.user.id,
            item_id=item_id,
            pool=self.pool,
        )
        await interaction.response.send_message(status, ephemeral=True)


class AuctionItemSearchBasePages(KumikoPages):
    def __init__(self, entries, *, ctx: commands.Context, per_page: int = 10):
        super().__init__(SimplePageSource(entries, per_page=per_page), ctx=ctx)
        self.embed = discord.Embed(
            title="Results", colour=discord.Colour.from_rgb(219, 171, 255)
        )
