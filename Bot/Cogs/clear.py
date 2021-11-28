import discord
from Cogs import plugin_tools
from discord.ext import commands


class clearMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(
        name="clear",
        help="Clears number of messages specified from the channel in which the command was called",
    )
    async def clear(self, ctx, number_of_messages: int):
        await ctx.channel.purge(limit=number_of_messages + 1)
        await ctx.send(
            embed=plugin_tools.fast_embed(
                f"{number_of_messages} messages were deleted"
            ),
            delete_after=3,
        )

    @clear.error
    async def on_message_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingRequiredArgument):
            embedVar = discord.Embed(color=discord.Color.from_rgb(255, 51, 51))
            embedVar.description = f"Missing a required argument: {error.param}"
            embedVar.set_footer(
                text="This only clears messages **before** this command is used"
            )
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)


def setup(bot):
    bot.add_cog(clearMessages(bot))
