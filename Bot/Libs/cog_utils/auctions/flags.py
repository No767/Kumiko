from discord.ext import commands


class ListingFlag(commands.FlagConverter):
    amount: int = commands.flag(
        default=1, aliases=["a"], description="The amount of items to list"
    )
