import discord
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.economy import getUser
from Libs.ui.economy import RegisterView
from Libs.utils import Embed


class Economy(commands.Cog):
    """Earn, sell, and interact with Kumiko's economy!"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        super().__init__()

    @commands.hybrid_group(name="marketplace")
    async def eco(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @eco.command(name="buy")
    async def marketplaceBuy(self, ctx: commands.Context) -> None:
        """Buy an item from the marketplace"""
        await ctx.send("Buy")

    @commands.hybrid_command(name="register")
    async def register(self, ctx: commands.Context) -> discord.Message:
        """Create an account for the economy"""
        view = RegisterView()
        embed = Embed(
            title="Register",
            description="Register for the economy! Before you do so, please make sure to follow the TOS. By registering, you are agreeing to use these services.",
        )
        return await ctx.send(embed=embed, view=view)

    @commands.hybrid_command(name="wallet")
    async def wallet(self, ctx: commands.Context) -> discord.Message:
        """Checks your wallet"""
        user = await getUser(ctx.author.id)
        if user is None:
            return await ctx.send(
                embed=Embed(
                    title="No Wallet", description="You don't have a wallet yet!"
                )
            )
        embed = Embed(
            title=f"{ctx.author.name}'s Wallet",
            description=f"Balance: {user['petals']}",
        )
        return await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Economy(bot))
