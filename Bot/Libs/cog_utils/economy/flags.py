from discord.ext import commands


class ItemFlags(commands.FlagConverter):
    price: int = commands.flag(
        aliases=["p"], description="The price of the item to set"
    )
    amount: int = commands.flag(
        aliases=["a"], description="The amount of the item to output"
    )


class PurchaseFlags(commands.FlagConverter):
    amount: int = commands.flag(
        aliases=["a"], default=1, description="The amount of items to purchase"
    )
