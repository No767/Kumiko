import discord
from dateutil.parser import ParserError
from discord.ext import commands


class InteractionFailureHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def fullException(self, obj):
        module = obj.__class__.__module__
        if module is None or module == str.__class__.__module__:
            return obj.__class__.__name__
        return module + "." + obj.__class__.__name__

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = int(error.retry_after) % (24 * 3600)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            await ctx.respond(
                embed=discord.Embed(
                    description=f"This command is currently on cooldown. Try again in {hours} hour(s), {minutes} minute(s), and {seconds} second(s)."
                )
            )
        elif isinstance(error, commands.MissingPermissions):
            missingPerms = (
                str(error.missing_permissions)
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
            )
            await ctx.respond(
                embed=discord.Embed(
                    description=f"You are missing the following permissions: {missingPerms}"
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            missingPerms = (
                str(error.missing_permissions)
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
            )
            await ctx.respond(
                embed=discord.Embed(
                    description=f"Kumiko is missing the following permissions: {missingPerms}"
                )
            )
        elif isinstance(error, discord.ApplicationCommandInvokeError):
            if isinstance(error, ParserError):
                await ctx.respond(
                    "It seems like you probably have inputted the incorrect format for the datetime. Some examples of this include: `August 5, 2022 12:00`, `3-4-2022 13:30`, `2022-08-03 12:00 pm`"
                )
            else:
                errorEmbed = discord.Embed(
                    title="An error has occured",
                    color=discord.Color.from_rgb(255, 41, 41),
                )
                errorEmbedHeader = "Uh oh! It seems like the command ran into an issue! For support, please visit Kumiko's Support Server to get help!"
                errorEmbed.description = f"{errorEmbedHeader}\n\n**Error:** ```{error.original}```\n**Full Exception Message:**\n```{self.fullException(error.original)}: {str(error.original)}```"
                await ctx.respond(embed=errorEmbed)


def setup(bot):
    bot.add_cog(InteractionFailureHandler(bot))
