import traceback

from discord.ext import commands
from kumikocore import KumikoCore
from Libs.errors import EconomyDisabled, ValidationError
from Libs.utils import ErrorEmbed


class ErrorHandler(commands.Cog):
    """Cog to handle errors"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    def produce_error_embed(self, error: commands.CommandError):
        embed = ErrorEmbed()
        desc = (
            "Uh oh! It seems like the command ran into an issue! For support, please visit Kumiko's Support Server to get help!\n\n",
            f"**Error**: \n```{''.join(traceback.format_exception_only(error))}```",
        )
        embed.description = "\n".join(desc)
        return embed

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Handles any errors on regular prefixed commands

        Args:
            ctx (commands.Context): Commands context
            error (commands.CommandError): The error that is being propagated
        """
        # if isinstance(error, commands.CommandOnCooldown):
        #     seconds = int(error.retry_after) % (24 * 3600)
        #     hours = seconds // 3600
        #     seconds %= 3600
        #     minutes = seconds // 60
        #     seconds %= 60
        #     await ctx.send(
        #         embed=Embed(
        #             description=f"This command is currently on cooldown. Try again in {hours} hour(s), {minutes} minute(s), and {seconds} second(s)."
        #         )
        #     )
        if isinstance(error, commands.CommandInvokeError) or isinstance(
            error, commands.HybridCommandError
        ):
            await ctx.send(embed=self.produce_error_embed(error))
        elif isinstance(error, commands.CommandNotFound):
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Command Not Found"
            errorEmbed.description = (
                "The command you were looking for could not be found"
            )
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.NotOwner):
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Command requires the owner to run"
            errorEmbed.description = (
                "The command can only be ran by the owner of the guild"
            )
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.MissingPermissions):
            missingPerms = ", ".join(error.missing_permissions).rstrip(",")
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Missing Permissions"
            errorEmbed.description = (
                f"You are missing the following permissions: {missingPerms}"
            )
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Missing Required Argument"
            errorEmbed.description = (
                f"You are missing the following argument(s): {error.param.name}"
            )
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, ValidationError):
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Validation Error"
            errorEmbed.description = str(error)
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, EconomyDisabled):
            errorEmbed = ErrorEmbed(title="Economy Disabled")
            errorEmbed.description = str(error)
            await ctx.send(embed=errorEmbed)
        else:
            await ctx.send(embed=self.produce_error_embed(error))


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(ErrorHandler(bot))
