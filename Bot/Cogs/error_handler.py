import traceback

from discord.ext import commands
from kumikocore import KumikoCore
from Libs.errors import EconomyDisabledError, RedirectsDisabledError, ValidationError
from Libs.utils import ErrorEmbed


class ErrorHandler(commands.Cog):
    """Cog to handle errors"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    def produce_error_embed(self, error: commands.CommandError):
        embed = ErrorEmbed()
        error_traceback = "\n".join(traceback.format_exception_only(type(error), error))
        desc = (
            "Uh oh! It seems like the command ran into an issue! For support, please visit Kumiko's Support Server to get help!\n\n",
            f"**Error**: \n```{error_traceback}```",
        )
        embed.description = "\n".join(desc)
        return embed

    def create_premade_embed(self, title: str, description: str):
        embed = ErrorEmbed()
        embed.title = title
        embed.description = description
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
        if isinstance(error, commands.CommandInvokeError) or isinstance(
            error, commands.HybridCommandError
        ):
            await ctx.send(embed=self.produce_error_embed(error))
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(
                embed=self.create_premade_embed(
                    "Command Not Found",
                    "The command you were looking for could not be found",
                )
            )
        elif isinstance(error, commands.NotOwner):
            await ctx.send(
                embed=self.create_premade_embed(
                    "Command requires the owner to run",
                    "The command can only be ran by the owner of the guild",
                )
            )
        elif isinstance(error, commands.MissingPermissions):
            missing_perms = ", ".join(error.missing_permissions).rstrip(",")
            await ctx.send(
                embed=self.create_premade_embed(
                    "Missing Permissions",
                    f"You are missing the following permissions: {missing_perms}",
                )
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed=self.create_premade_embed(
                    "Missing Requireed Argument",
                    f"You are missing the following argument(s): {error.param.name}",
                )
            )
        elif isinstance(error, ValidationError):
            await ctx.send(
                embed=self.create_premade_embed("Validation Error", str(error))
            )
        elif isinstance(error, EconomyDisabledError):
            await ctx.send(
                embed=self.create_premade_embed("Economy Disabled", str(error))
            )
        elif isinstance(error, RedirectsDisabledError):
            await ctx.send(
                embed=self.create_premade_embed("Redirects Disabled", str(error))
            )
        else:
            await ctx.send(embed=self.produce_error_embed(error))


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(ErrorHandler(bot))
