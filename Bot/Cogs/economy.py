import discord
from discord.ext import commands
from Libs.economy import getUser
from Libs.utils import Embed
from prisma.models import User


class Economy(commands.Cog):
    """Earn, sell, and interact with Kumiko's economy!"""

    def __init__(self, bot: commands.Bot) -> None:
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
        doesUserExist = (
            await User.prisma().count(where={"id": ctx.author.id}, take=1) == 1
        )
        if doesUserExist:
            return await ctx.send(
                embed=Embed(
                    title="Already Registered",
                    description="You already have an account!",
                )
            )
        await User.prisma().create(data={"id": ctx.author.id, "name": ctx.author.name})
        return await ctx.send(
            embed=Embed(
                title="Registered", description="You have successfully registered!"
            )
        )

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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Economy(bot))
