import discord
from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.economy import PurchaseFlags, is_economy_enabled
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
    @commands.hybrid_group(name="marketplace")
    async def marketplace(self, ctx: commands.Context) -> None:
        """List the items available for purchase"""
        raise NotImplementedError

    # TODO - Also check if the payment is valid. aka it must be higher or equal to the price and amount
    # also validate all areas. if there are 0, it is out of stock, etc
    @is_economy_enabled()
    @marketplace.command(name="buy", aliases=["purchase"], usage="amount: <int>")
    @app_commands.describe(name="The name of the item to buy")
    async def buy(
        self,
        ctx: commands.Context,
        name: Annotated[str, commands.clean_content],
        *,
        flags: PurchaseFlags
    ) -> None:
        """Buy an item from the marketplace"""
        query = """
        SELECT eco_item.id, eco_item.price, eco_item.amount, eco_item.producer_id
        FROM eco_item_lookup
        INNER JOIN eco_item ON eco_item.id = eco_item_lookup.item_id
        WHERE eco_item_lookup.guild_id=$1 AND LOWER(eco_item_lookup.name)=$2 AND eco_item_lookup.owner_id IS NULL;
        """
        setOwnerQuery = """
        WITH item_update AS (
            UPDATE eco_item
            SET owner_id = $2, amount = $4
            WHERE guild_id = $1 AND name = $3
            RETURNING id
        )
        UPDATE eco_item_lookup
        SET owner_id = $2
        WHERE id = (SELECT id FROM item_update);
        """
        updateBalanceQuery = """
        UPDATE eco_user
        SET petals = $2
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
            async with conn.transaction():
                await conn.execute(setOwnerQuery, ctx.guild.id, ctx.author.id, name.lower(), records["amount"] - flags.amount)  # type: ignore
                await conn.execute(
                    updateBalanceQuery,
                    records["producer_id"],
                    records["price"] + totalPrice,
                )
                await conn.execute(
                    updateBalanceQuery, ctx.author.id, records["price"] - totalPrice
                )
            await ctx.send("Purchased item")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Marketplace(bot))
