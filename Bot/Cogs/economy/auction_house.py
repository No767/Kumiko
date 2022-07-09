from discord.commands import Option, SlashCommandGroup
from discord.ext import commands


class AuctionHouseV1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    auctionHouse = SlashCommandGroup("auction", "Auction off your highest items here")

    @auctionHouse.command(name="bid", guild_ids=[970159505390325842])
    async def bindForPrice(self, ctx, *, price: Option(str, "The price to bid")):
        await ctx.respond(price)


def setup(bot):
    bot.add_cog(AuctionHouseV1(bot))
