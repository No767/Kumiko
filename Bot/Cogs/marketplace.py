import discord
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.economy import PurchaseFlags, is_economy_enabled
from Libs.cog_utils.marketplace import formatOptions, getItem, isPaymentValid
from Libs.ui.marketplace import ItemPages, SimpleSearchItemPages
from Libs.utils import Embed, get_or_fetch_member
from typing_extensions import Annotated


class Marketplace(commands.Cog):
    """Shop for items and others produced from the Jobs module

    This is the module to buy and sell items produced from the Jobs module.
    """

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:shop:1132982447177478214>")

    @is_economy_enabled()
    @commands.hybrid_group(name="marketplace", fallback="list")
    async def marketplace(self, ctx: commands.Context) -> None:
        """List the items available for purchase"""
        query = """
        SELECT eco_item.id, eco_item.name, eco_item.description, eco_item.price, eco_item.amount, eco_item.producer_id
        FROM eco_item_lookup
        INNER JOIN eco_item ON eco_item.id = eco_item_lookup.item_id
        WHERE eco_item.guild_id = $1;
        """
        rows = await self.pool.fetch(query, ctx.guild.id)  # type: ignore
        if len(rows) == 0:
            await ctx.send("No items available")
            return

        pages = ItemPages(entries=rows, ctx=ctx, per_page=1)
        await pages.start()

    @is_economy_enabled()
    @marketplace.command(name="buy", aliases=["purchase"], usage="amount: <int>")
    @app_commands.describe(name="The name of the item to buy")
    async def buy(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        *,
        flags: PurchaseFlags,
    ) -> None:
        """Buy an item from the marketplace"""
        query = """
        SELECT eco_item.id, eco_item.price, eco_item.amount, eco_item.producer_id
        FROM eco_item_lookup
        INNER JOIN eco_item ON eco_item.id = eco_item_lookup.item_id
        WHERE eco_item_lookup.guild_id=$1 AND LOWER(eco_item_lookup.name)=$2;
        """
        # If you already bought that item and someone else bought it
        # then the amount owned will go to you
        # big bug
        # honestly a many-to-many relationship might actually be needed here
        # TODO - Please find some way to fix this
        purchaseItem = """
        WITH item_update AS (
            UPDATE eco_item
            SET amount = $4
            WHERE guild_id = $1 AND name = $3
            RETURNING id
        )
        INSERT INTO user_inv (owner_id, guild_id, amount_owned, item_id)
        VALUES ($2, $1, $5, (SELECT id FROM item_update))
        ON CONFLICT (item_id) DO UPDATE
        SET amount_owned = user_inv.amount_owned + excluded.amount_owned;
        """
        updateBalanceQuery = """
        UPDATE eco_user
        SET petals = petals + $2
        WHERE id = $1;
        """
        updatePurchaserQuery = """
        UPDATE eco_user
        SET petals = petals - $2
        WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetchrow(query, ctx.guild.id, name.lower())  # type: ignore
            if rows is None:
                await ctx.send(
                    "The item you are looking for does not exist, or is already bought. Please try again"
                )
                return
            records = dict(rows)
            if records["producer_id"] == ctx.author.id:
                await ctx.send(
                    "You can't buy your own goods! Buy something else instead"
                )
                return
            totalPrice = records["price"] * flags.amount
            if await isPaymentValid(records, ctx.author.id, flags.amount, conn) is True:
                async with conn.transaction():
                    await conn.execute(purchaseItem, ctx.guild.id, ctx.author.id, name.lower(), records["amount"] - flags.amount, flags.amount)  # type: ignore
                    await conn.execute(
                        updateBalanceQuery,
                        records["producer_id"],
                        totalPrice,
                    )
                    await conn.execute(updatePurchaserQuery, ctx.author.id, totalPrice)
                await ctx.send(f"Purchased item `{name}` for `{totalPrice}`")
            else:
                await ctx.send(
                    "The payment is invalid. This is due to the following:\n"
                    "1. The amount you requested is higher than the amount in stock\n"
                    "2. You don't have enough funds to make the purchase\n"
                    "3. There are no remaining in stock\n"
                )
                return

    @is_economy_enabled()
    @marketplace.command(name="info")
    @app_commands.describe(name="The name of the item to search for")
    async def info(
        self, ctx: commands.Context, *, name: Annotated[str, commands.clean_content]
    ) -> None:
        """Provides info about an item listed on the marketplace"""
        item = await getItem(ctx.guild.id, name, self.bot.pool)  # type: ignore
        if isinstance(item, list):
            await ctx.send(formatOptions(item) or ".")
            return

        member = await get_or_fetch_member(ctx.guild, item["producer_id"])  # type: ignore
        if member is None or item is None:
            await ctx.send("There was an issue")
            return
        record = item
        embed = Embed()
        embed.set_author(name=record["name"], icon_url=member.display_avatar.url)
        embed.set_footer(text=f"ID: {record['id']} | Created at")
        embed.timestamp = record["created_at"]
        embed.description = record["description"]
        embed.add_field(name="Price", value=record["price"])
        embed.add_field(name="Amount", value=record["amount"])
        await ctx.send(embed=embed)

    @is_economy_enabled()
    @marketplace.command(name="search")
    @app_commands.describe(query="The name of the item to look for")
    async def search(
        self, ctx: commands.Context, *, query: Annotated[str, commands.clean_content]
    ) -> None:
        """Searches for an item in the marketplace"""
        if len(query) < 3:
            await ctx.send("The query must be at least 3 characters")
            return

        sql = """
        SELECT id, name
        FROM eco_item_lookup
        WHERE guild_id=$1 AND name % $2
        ORDER BY similarity(name, $2) DESC
        LIMIT 100;
        """
        records = await self.pool.fetch(sql, ctx.guild.id, query)  # type: ignore
        if records:
            pages = SimpleSearchItemPages(entries=records, per_page=20, ctx=ctx)
            await pages.start()
        else:
            await ctx.send("No items found")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Marketplace(bot))
