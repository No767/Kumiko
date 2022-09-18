import discord
from discord.ext import commands


class cooldownChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # later add the actual amount of time left...
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
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(
                embed=discord.Embed(
                    description=f"You are missing the following permissions: {error.missing_permissions}"
                )
            )
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond(
                embed=discord.Embed(
                    description=f"You are missing the following permissions: {error.missing_permissions}"
                )
            )


def setup(bot):
    bot.add_cog(cooldownChecker(bot))
