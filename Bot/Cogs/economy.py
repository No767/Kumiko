import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.economy import RefundFlags, is_economy_enabled
from Libs.ui.economy import LeaderboardPages, RegisterView, UserInvPages
from Libs.utils import ConfirmEmbed, Embed


class Economy(commands.Cog):
    """Trade, earn, and gamble your way to the top!

    This is Kumiko's flagship module.
    """

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool
        self.local_economy_key = "$.local_economy"

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:upward_stonks:739614245997641740>")

    @property
    def configurable(self) -> bool:
        return True

    @commands.hybrid_group(name="eco", aliases=["economy"])
    async def eco(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @is_economy_enabled()
    @eco.command(name="wallet", aliases=["bal", "balance"])
    async def wallet(self, ctx: commands.Context) -> None:
        """View your eco wallet"""
        sql = """
        SELECT rank, petals, created_at
        FROM eco_user
        WHERE id = $1;
        """
        user = await self.pool.fetchrow(sql, ctx.author.id)
        if user is None:
            await ctx.send(
                f"You have not created an economy account yet! Run `{ctx.prefix}eco register` to create one."
            )
            return
        user_record = dict(user)
        embed = Embed()
        embed.set_author(
            name=f"{ctx.author.display_name}'s Balance",
            icon_url=ctx.author.display_avatar.url,
        )
        embed.set_footer(text="Created at")
        embed.timestamp = user_record["created_at"]
        embed.add_field(name="Rank", value=user_record["rank"], inline=True)
        embed.add_field(name="Petals", value=user_record["petals"], inline=True)
        await ctx.send(embed=embed)

    @is_economy_enabled()
    @eco.command(name="register")
    async def register(self, ctx: commands.Context) -> None:
        """Register for an economy account"""
        view = RegisterView(ctx, self.pool)
        embed = ConfirmEmbed()
        embed.description = "Do you want to make an account? The account can only be accessed from your current guild"
        await ctx.send(embed=embed, view=view)

    @is_economy_enabled()
    @eco.command(name="inventory", aliases=["inv"])
    async def inventory(self, ctx: commands.Context) -> None:
        """View your inventory"""
        query = """
        SELECT eco_item.id, eco_item.name, eco_item.description, eco_item.price, user_inv.amount_owned, eco_item.producer_id
        FROM user_inv 
        INNER JOIN eco_item ON eco_item.id = user_inv.item_id
        WHERE eco_item.guild_id = $1 AND user_inv.owner_id = $2;
        """
        rows = await self.pool.fetch(query, ctx.guild.id, ctx.author.id)  # type: ignore
        if len(rows) == 0:
            await ctx.send("No items available")
            return

        pages = UserInvPages(entries=rows, ctx=ctx, per_page=1, pool=self.pool)
        await pages.start()

    @is_economy_enabled()
    @eco.command(name="top", aliases=["baltop"])
    async def top(self, ctx: commands.Context) -> None:
        """View the top players in your server"""
        query = """
        SELECT id, rank, petals
        FROM eco_user
        ORDER BY petals ASC
        LIMIT 100;
        """
        rows = await self.pool.fetch(query)
        if len(rows) == 0:
            await ctx.send("No users available")
            return

        pages = LeaderboardPages(entries=rows, ctx=ctx, per_page=10)
        await pages.start()

    @is_economy_enabled()
    @eco.command(name="refund", aliases=["return"])
    async def refund(self, ctx: commands.Context, *, flags: RefundFlags) -> None:
        """Refunds your item, but you will only get 75% of the original price back"""
        sql = """
        SELECT eco_item.name, eco_item.price, user_inv.owner_id, user_inv.amount_owned, user_inv.item_id
        FROM user_inv
        INNER JOIN eco_item ON eco_item.id = user_inv.item_id
        WHERE user_inv.owner_id =  $1 AND user_inv.guild_id = $2 AND eco_item.name = $3;
        """
        subtract_owned_items = """
        UPDATE user_inv
        SET amount_owned = amount_owned - $1
        WHERE owner_id = $2 AND guild_id = $3 AND item_id = $4;
        """
        add_back_items_to_stock = """
        UPDATE eco_item
        SET amount = amount + $1
        WHERE id = $2;
        """
        add_back_price = """
        UPDATE eco_user
        SET petals = petals - $1
        WHERE id = $2;
        """
        assert (
            ctx.guild is not None
        )  # Apparently this fixes the ctx.guild.id being None thing
        async with self.pool.acquire() as conn:
            rows = await conn.fetchrow(
                sql, ctx.author.id, ctx.guild.id, flags.name.lower()
            )
            if rows is None:
                await ctx.send("You do not own this item!")
                return
            records = dict(rows)
            refund_price = ((records["price"] * flags.amount) / 4) * 3
            if flags.amount > records["amount_owned"]:
                # Here we want to basically make sure that if the user requests more, then we don't take more than we need to
                # TODO: Add that math here
                await ctx.send("You do not own that many items!")
                return
            async with conn.transaction():
                await conn.execute(
                    subtract_owned_items,
                    flags.amount,
                    ctx.author.id,
                    ctx.guild.id,
                    records["item_id"],
                )
                await conn.execute(
                    add_back_items_to_stock, flags.amount, records["item_id"]
                )
                await conn.execute(add_back_price, refund_price, ctx.author.id)

            await ctx.send("Successfully refunded your item!")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Economy(bot))
