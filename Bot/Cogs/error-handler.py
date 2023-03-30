from typing import Union

from discord.app_commands.errors import CommandInvokeError
from discord.ext import commands
from Libs.errors import HTTPError, KumikoException, NoItemsError, NotFoundError
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

    def getErrorCatches(self, error: Union[KumikoException, Exception]) -> ErrorEmbed:
        errorEmbed = ErrorEmbed()
        if isinstance(error, HTTPError):
            errorEmbed.description = "There was an HTTP error, and the request could not be made. Please try again later or contact support staff in Kumiko's support server for help."
            errorEmbed.add_field(name="Status", value=error.status, inline=False)
            errorEmbed.add_field(
                name="Message", value=error.message or "...", inline=False
            )
            return errorEmbed
        elif isinstance(error, NotFoundError):
            errorEmbed.description = "The resource you were looking for could not be found. Please try again later"
            return errorEmbed
        elif isinstance(error, NoItemsError):
            errorEmbed.description = (
                "The item you were looking for doesn't exist. Please try again later."
            )
            return errorEmbed
        else:
            errorEmbed.add_field(name="Error", value=str(error), inline=False)
            errorEmbed.add_field(
                name="Full Exception Message",
                value=f"{self.fullException(error)}: {error}",
                inline=False,
            )
        return errorEmbed

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
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=self.getErrorCatches(error.original))
        elif isinstance(error, commands.HybridCommandError):
            if isinstance(error.original, CommandInvokeError):
                await ctx.send(embed=self.getErrorCatches(error.original.original))
        elif isinstance(error, commands.DisabledCommand):
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Command Disabled"
            errorEmbed.description = (
                "The command you were looking for is currently disabled"
            )
            await ctx.send(embed=errorEmbed)
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
        elif isinstance(error, commands.BotMissingPermissions):
            missingPerms = ", ".join(error.missing_permissions).rstrip(",")
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Kumiko is missing permissions"
            errorEmbed.description = (
                f"Kumiko is missing the following permissions: {missingPerms}"
            )
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.MissingAnyRole):
            missingRoles = ", ".join(
                str(roles) for roles in error.missing_roles
            ).rstrip(",")
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Missing Roles"
            errorEmbed.description = (
                f"You are missing the following role(s): {missingRoles}"
            )
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.BotMissingAnyRole):
            missingRoles = ", ".join(
                str(roles) for roles in error.missing_roles
            ).rstrip(",")
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Kumiko is missing roles"
            errorEmbed.description = (
                f"Kumiko is missing the following role(s): {missingRoles}"
            )
            await ctx.send(embed=errorEmbed)
        elif isinstance(error, commands.MissingRequiredArgument):
            errorEmbed = ErrorEmbed()
            errorEmbed.title = "Missing Required Argument"
            errorEmbed.description = (
                f"You are missing the following argument(s): {error.param.name}"
            )
            await ctx.send(embed=errorEmbed)
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
