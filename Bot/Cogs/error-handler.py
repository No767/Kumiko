from discord.ext import commands
from Libs.utils import Embed, ErrorEmbed


class ErrorHandler(commands.Cog):
    """Cog to handle errors"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def fullException(self, obj):
        module = obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return obj.__class__.__name__
        return module + "." + obj.__class__.__name__

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Handles any errors on regular prefixed commands

        Args:
            ctx (commands.Context): Commands context
            error (commands.CommandError): The error that is being propagated
        """
        if isinstance(error, commands.CommandOnCooldown):
            seconds = int(error.retry_after) % (24 * 3600)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            await ctx.send(
                embed=Embed(
                    description=f"This command is currently on cooldown. Try again in {hours} hour(s), {minutes} minute(s), and {seconds} second(s)."
                )
            )
        else:
            errorEmbed = ErrorEmbed()
            errorEmbed.add_field(name="Error", value=str(error), inline=False)
            errorEmbed.add_field(
                name="Full Exception Message",
                value=f"{self.fullException(error)}: {error}",
                inline=False,
            )
            await ctx.send(embed=errorEmbed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))
