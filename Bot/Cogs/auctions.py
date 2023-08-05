import datetime

from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.auctions import (
    ListingFlag,
    add_more_to_auction,
    create_auction,
    delete_auction,
    format_options,
    obtain_item_info,
)
from Libs.cog_utils.economy import is_economy_enabled
from Libs.ui.auctions import AuctionPages, AuctionSearchPages, OwnedAuctionPages
from Libs.utils import Embed
from typing_extensions import Annotated


class Auctions(commands.Cog):
    """List unwanted items away here"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<:auction_house:1136906394323398749>")

    @is_economy_enabled()
    @commands.hybrid_group(
        name="auctions", fallback="view", aliases=["auction-house", "ah"]
    )
    async def auctions(self, ctx: commands.Context) -> None:
        """List the items available for purchase"""
        sql = """
        SELECT eco_item.id, eco_item.name, eco_item.description, auction_house.user_id, auction_house.amount_listed, auction_house.listed_price, auction_house.listed_at
        FROM auction_house
        INNER JOIN eco_item ON eco_item.id = auction_house.item_id
        WHERE auction_house.guild_id = $1;
        """
        if ctx.guild is None:
            await ctx.send("You can't use this in DMs")
            return
        rows = await self.pool.fetch(sql, ctx.guild.id)

        if len(rows) == 0:
            await ctx.send("No records found")
            return

        pages = AuctionPages(entries=rows, ctx=ctx, per_page=1)
        await pages.start()

    @is_economy_enabled()
    @auctions.command(name="create", aliases=["make"], usage="amount: <int>")
    @app_commands.describe(name="The name of the item to list for purchase")
    async def create(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        *,
        flags: ListingFlag,
    ) -> None:
        """Lists the given item for purchase"""
        if ctx.guild is None:
            await ctx.send("DMs can't be used here")
            return
        status = await create_auction(
            guild_id=ctx.guild.id,
            user_id=ctx.author.id,
            amount_requested=flags.amount,
            item_id=None,
            item_name=name,
            pool=self.bot.pool,
        )
        await ctx.send(status)

    @is_economy_enabled()
    @auctions.command(name="delete", aliases=["remove"])
    @app_commands.describe(name="The name of the item to list for removal")
    async def delete(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ) -> None:
        """List the items available for purchase"""
        if ctx.guild is None:
            await ctx.send("DMs can't be used here")
            return
        status = await delete_auction(
            guild_id=ctx.guild.id,
            user_id=ctx.author.id,
            item_name=name,
            pool=self.bot.pool,
        )
        await ctx.send(status)

    @is_economy_enabled()
    @auctions.command(name="update", aliases=["edit"], usage="amount: <int>")
    @app_commands.describe(name="The name of the item you want to update")
    async def update(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        *,
        flags: ListingFlag,
    ) -> None:
        """Updates the listed amount for the given item"""
        if ctx.guild is None:
            await ctx.send("DMs can't be used here")
            return
        status = await add_more_to_auction(
            guild_id=ctx.guild.id,
            user_id=ctx.author.id,
            amount_requested=flags.amount,
            item_name=name,
            pool=self.bot.pool,
        )
        await ctx.send(status)

    @is_economy_enabled()
    @auctions.command(name="owned")
    async def owned(self, ctx: commands.Context) -> None:
        """Get items listed by you"""
        sql = """
        SELECT eco_item.id, eco_item.name, eco_item.description, auction_house.amount_listed, auction_house.listed_price, auction_house.listed_at
        FROM auction_house
        INNER JOIN eco_item ON eco_item.id = auction_house.item_id
        WHERE auction_house.user_id = $1 AND auction_house.guild_id = $2;
        """
        if ctx.guild is None:
            await ctx.send("You can't use this in DMs")
            return
        rows = await self.pool.fetch(sql, ctx.author.id, ctx.guild.id)

        pages = OwnedAuctionPages(entries=rows, ctx=ctx, per_page=1, pool=self.pool)
        await pages.start()

    @is_economy_enabled()
    @auctions.command(name="search")
    async def search(
        self, ctx: commands.Context, *, query: Annotated[str, commands.clean_content]
    ) -> None:
        """Searches for the item listed in the Auction House"""
        sql = """
        SELECT eco_item.id AS item_id, eco_item.name as item_name, auction_house.user_id, auction_house.amount_listed
        FROM auction_house
        INNER JOIN eco_item ON eco_item.name % $2
        WHERE auction_house.guild_id=$1
        ORDER BY similarity(eco_item.name, $2) DESC
        LIMIT 100;
        """
        if ctx.guild is None:
            await ctx.send("You can't use this in DMs")
            return
        rows = await self.pool.fetch(sql, ctx.guild.id, query)

        if len(rows) == 0:
            await ctx.send("No records found")
            return

        pages = AuctionSearchPages(entries=rows, ctx=ctx, per_page=10)
        await pages.start()

    @is_economy_enabled()
    @auctions.command(name="info")
    @app_commands.describe(name="The name of the item to look at")
    async def info(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Provides info about the given item"""
        if ctx.guild is None:
            await ctx.send("This cannot be used in DMs")
            return
        item_info = await obtain_item_info(
            guild_id=ctx.guild.id, name=name, pool=self.pool
        )
        if item_info is None:
            await ctx.send("The item was never found")
            return
        if isinstance(item_info, list):
            await ctx.send(format_options(item_info) or ".")
            return
        embed = Embed()
        embed.title = item_info["name"]
        embed.description = item_info["description"]
        embed.add_field(name="Amount Listed", value=item_info["amount_listed"])
        embed.add_field(name="Listed Price", value=item_info["listed_price"])
        embed.add_field(name="Listed By", value=f"<@{item_info['user_id']}>")
        embed.set_footer(text="Listed at")
        embed.timestamp = item_info["listed_at"].replace(tzinfo=datetime.timezone.utc)
        await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Auctions(bot))
