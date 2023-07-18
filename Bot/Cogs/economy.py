import asyncpg
import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cache import KumikoCache

# from Libs.cog_utils.economy import is_economy_enabled
from Libs.errors import EconomyDisabled
from Libs.ui.economy import RegisterView
from Libs.utils import ConfirmEmbed, Embed
from Libs.utils.pages import EmbedListSource, KumikoPages


async def predicate(ctx: commands.Context):
    if ctx.guild is None:
        raise EconomyDisabled
    key = f"cache:kumiko:{ctx.guild.id}:eco_status"
    cache = KumikoCache(connection_pool=ctx.bot.redis_pool)
    if await cache.cacheExists(key=key):
        result = await cache.getBasicCache(key=key)
        parsedRes = bool(int(result))  # type: ignore
        if parsedRes is False:
            raise EconomyDisabled
        return parsedRes
    else:
        pool: asyncpg.Pool = ctx.bot.pool
        res = await pool.fetchval(
            "SELECT local_economy FROM guild WHERE id = $1;", ctx.guild.id
        )
        if res is True:
            await cache.setBasicCache(key=key, value=str(1), ttl=None)
            return True
        await cache.setBasicCache(key=key, value=str(0), ttl=None)
        raise EconomyDisabled


class Economy(commands.Cog):
    """Trade, earn, and gamble your way to the top!

    This is Kumiko's flagship module.
    """

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool
        self.redis_pool = self.bot.redis_pool

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:upward_stonks:739614245997641740>")

    @commands.hybrid_group(name="eco", aliases=["economy"])
    async def eco(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    # Throw checks on these later
    @eco.command(name="enable")
    async def enable(self, ctx: commands.Context) -> None:
        """Enables the economy module for your server"""
        key = f"cache:kumiko:{ctx.guild.id}:config"  # type: ignore
        cache = KumikoCache(connection_pool=self.redis_pool)
        query = """
        UPDATE guild
        SET local_economy = $2
        WHERE id = $1;
        """
        result = await cache.getJSONCache(key=key, path=".local_economy")
        if result is True:
            await ctx.send("Economy is already enabled for your server!")
            return
        else:
            await self.pool.execute(query, ctx.guild.id, True)  # type: ignore
            await cache.setJSONCache(key=key, value={"local_economy": True}, ttl=None)
            await ctx.send("Enabled economy!")
            return

    @eco.command(name="disable")
    async def disable(self, ctx: commands.Context) -> None:
        """Disables the economy module for your server"""
        key = f"cache:kumiko:{ctx.guild.id}:config"  # type: ignore
        cache = KumikoCache(connection_pool=self.redis_pool)
        query = """
        UPDATE guild
        SET local_economy = $2
        WHERE id = $1;
        """
        if await cache.cacheExists(key=key):
            result = await cache.getJSONCache(key=key, path=".local_economy")
            if result is True:
                await self.pool.execute(query, ctx.guild.id, False)  # type: ignore
                await cache.setJSONCache(
                    key=key, value={"local_economy": False}, ttl=None
                )
                await ctx.send(
                    "Economy is now disabled for your server. Please enable it first."
                )
                return
            else:
                await ctx.send("Economy is already disabled for your server!")
                return

    # @is_economy_enabled()
    @commands.check(predicate)
    @eco.command(name="wallet", aliases=["bal", "balance"])
    async def wallet(self, ctx: commands.Context) -> None:
        """View your eco wallet"""
        sql = """
        SELECT rank, petals, created_at
        FROM eco_user
        WHERE id = $1;
        """
        user = await self.pool.fetchval(sql, ctx.author.id)
        if user is None:
            await ctx.send(
                f"You have not created an economy account yet! Run `{ctx.prefix}eco register` to create one."
            )
            return
        embed = Embed()
        embed.set_author(
            name=f"{ctx.author.display_name}'s Balance",
            icon_url=ctx.author.display_avatar.url,
        )
        embed.set_footer(text="Created at")
        embed.add_field(name="Rank", value=user["rank"], inline=False)
        embed.add_field(name="Balance", value=user["petal"], inline=False)
        await ctx.send(embed=embed)

    @eco.command(name="register")
    async def register(self, ctx: commands.Context) -> None:
        """Register for an economy account"""
        view = RegisterView(self.pool)
        embed = ConfirmEmbed()
        embed.description = "Do you want to make an account? The account can only be accessed from your current guild"
        await ctx.send(embed=embed, view=view)

    # @is_economy_enabled()
    @eco.command(name="inventory", aliases=["inv"])
    async def inventory(self, ctx: commands.Context) -> None:
        """View your inventory"""
        sql = """
        SELECT eco_item.id, eco_item.name, eco_item.description, eco_item.price, eco_item.amount
        FROM eco_item_lookup
        INNER JOIN eco_item ON eco_item.id = eco_item_lookup.item_id
        WHERE eco_item_lookup.owner_id = $1 AND eco_item_lookup.guild_id = $2;
        """
        rows = await self.pool.fetch(sql, ctx.author.id, ctx.guild.id)  # type: ignore
        if len(rows) == 0:
            await ctx.send("No items found")
            return
        embedList = [
            {
                "title": dict(row)["name"],
                "description": dict(row)["description"],
                "fields": [
                    {"name": "Price", "value": dict(row)["price"], "inline": True},
                    {"name": "Amount", "value": dict(row)["amount"], "inline": True},
                ],
            }
            for row in rows
        ]
        embedSource = EmbedListSource(entries=embedList, per_page=20)
        pages = KumikoPages(source=embedSource, ctx=ctx)
        await pages.start()


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Economy(bot))
