from discord.ext import commands


class JobOutputFlags(commands.FlagConverter):
    price: int = commands.flag(
        aliases=["p"], description="The price of the item to set"
    )
    amount: int = commands.flag(
        aliases=["a"], description="The amount of the item to output"
    )
