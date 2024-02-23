from discord.ext import commands


class JobOutputFlags(commands.FlagConverter):
    price: int = commands.flag(
        aliases=["p"], description="The price of the item to set"
    )
    amount_per_hour: int = commands.flag(
        aliases=["aph"], description="The amount of the item to output per hour"
    )


class JobListFlags(commands.FlagConverter):
    compact: bool = commands.flag(
        default=False, description="Whether to show a compacted page or not"
    )
