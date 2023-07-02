from discord import app_commands
from discord.ext import commands
from kumikocore import KumikoCore


# TODO - Straight up slap an GIN index on the prefixes column
# TODO - Add a bunch more commands (add, delete, update, etc)
class Prefixes(commands.Cog):
    """Kumiko's custom prefix manager! Set a custom prefix for your server!"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @commands.hybrid_group(name="prefixes")
    async def prefixes(self, ctx: commands.Context) -> None:
        """Base parent command for Prefixes - See the subcommands for more info"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    # TODO - Make sure that the prefixes is a list, not just one str
    @prefixes.command(name="update")
    @app_commands.describe(prefix="The new prefix to use")
    async def updatePrefixes(self, ctx: commands.Context, prefix: str) -> None:
        """Updates the prefix for your server

        Args:
            ctx (commands.Context): Base context
        """
        query = """
            UPDATE guild
            SET column = $1
            WHERE id = $2;
        """
        if ctx.guild is None:
            await ctx.send("You can't set a prefix in DMs!")
            return
        async with self.pool.acquire() as conn:
            await conn.execute(query, prefix, ctx.guild.id)
            self.bot.prefixes[ctx.guild.id] = prefix
            await ctx.send(f"Prefix updated to `{prefix}`")


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Prefixes(bot))
