import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.ui.economy import RegisterView
from Libs.utils import ConfirmEmbed, Embed


class Economy(commands.Cog):
    """Trade, earn, and gamble your way to the top!

    This is Kumiko's flagship module.
    """

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_property(self) -> discord.PartialEmoji:
        return discord.PartialEmoji.from_str("<:stonks:882025515697983528>")

    @commands.hybrid_group(name="eco", aliases=["economy"])
    async def eco(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @eco.command(name="balance", aliases=["bal"])
    async def balance(self, ctx: commands.Context) -> None:
        sql = """
        SELECT rank, petals, created_at
        FROM eco_user
        WHERE id = $1;
        """
        user = await self.pool.fetchval(sql, ctx.author.id)
        if user is None:
            await ctx.send(
                "You have not created an economy account yet! Run `>eco register` to create one."
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

    @eco.command(name="inventory", aliases=["inv"])
    async def inventory(self, ctx: commands.Context) -> None:
        """View your inventory"""
        sql = """
        SELECT eco_item.name, eco_item.fk_user
        FROM eco_item_lookup
        INNER JOIN eco_item ON eco_item.id = eco_item_lookup.item_id
        WHERE eco_item_lookup.owner_id = $1 AND eco_item_lookup.guild_id = $2;
        """


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Economy(bot))
