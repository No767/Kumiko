from discord import PartialEmoji, app_commands
from discord.ext import commands
from discord.utils import utcnow
from kumikocore import KumikoCore
from Libs.errors import ValidationError
from Libs.ui.prefix import DeletePrefixView
from Libs.utils import ConfirmEmbed, Embed, PrefixConverter, get_prefix


class Prefix(commands.Cog):
    """Manages custom prefixes for your server"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji(name="\U000025b6")

    @commands.hybrid_group(name="prefix")
    async def prefix(self, ctx: commands.Context) -> None:
        """Utilities to manage and view your server prefixes"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @prefix.command(name="update")
    @app_commands.describe(
        old_prefix="The old prefix to replace", new_prefix="The new prefix to use"
    )
    async def updatePrefixes(
        self, ctx: commands.Context, old_prefix: str, new_prefix: PrefixConverter
    ) -> None:
        """Updates the prefix for your server"""
        query = """
            UPDATE guild
            SET prefix = ARRAY_REPLACE(prefix, $1, $2)
            WHERE id = $3;
        """
        guild_id = ctx.guild.id  # type: ignore
        if old_prefix in self.bot.prefixes[guild_id]:
            async with self.pool.acquire() as conn:
                await conn.execute(query, old_prefix, new_prefix, guild_id)
                prefixes = self.bot.prefixes[guild_id][
                    :
                ]  # Shallow copy the list so we can safely perform operations on it
                idxSearch = [
                    idx for idx, item in enumerate(prefixes) if item == old_prefix
                ]
                prefixes[idxSearch[0]] = new_prefix
                self.bot.prefixes[guild_id] = prefixes
                await ctx.send(f"Prefix updated to `{new_prefix}`")
        else:
            await ctx.send("The prefix is not in the list of prefixes for your server")

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @prefix.command(name="add")
    @app_commands.describe(prefix="The new prefix to add")
    async def addPrefixes(self, ctx: commands.Context, prefix: PrefixConverter) -> None:
        """Adds new prefixes into your server"""
        prefixes = await get_prefix(self.bot, ctx.message)
        # validatePrefix(self.bot.prefixes, prefix) is False
        if len(prefixes) > 10:
            desc = "There was an validation issue. This is because of two reasons:\n- You have more than 10 prefixes for your server\n- Your prefix fails the validation rules"
            raise ValidationError(desc)

        query = """
            UPDATE guild
            SET prefix = ARRAY_APPEND(prefix, $1)
            WHERE id=$2;
        """
        async with self.pool.acquire() as conn:
            guildId = ctx.guild.id  # type: ignore # These are all done in an guild
            await conn.execute(query, prefix, guildId)
            self.bot.prefixes[guildId].append(prefix)
            await ctx.send(f"Added prefix: {prefix}")

    @commands.guild_only()
    @prefix.command(name="info")
    async def infoPrefixes(self, ctx: commands.Context) -> None:
        """Displays infos about the current prefix set on your server"""
        prefixes = await get_prefix(self.bot, ctx.message)
        cleanedPrefixes = ", ".join([f"`{item}`" for item in prefixes]).rstrip(",")
        embed = Embed()
        embed.description = f"**Current prefixes**\n{cleanedPrefixes}"
        embed.timestamp = utcnow()
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)  # type: ignore # LIES, LIES, AND LIES!!!
        await ctx.send(embed=embed)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.guild_only()
    @prefix.command(name="delete")
    @app_commands.describe(prefix="The prefix to delete")
    async def deletePrefixes(self, ctx: commands.Context, prefix: str) -> None:
        """Deletes a prefix from your server"""
        view = DeletePrefixView(bot=self.bot, prefix=prefix)
        embed = ConfirmEmbed()
        embed.description = f"Do you want to delete the following prefix: {prefix}"
        await ctx.send(embed=embed, view=view)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Prefix(bot))
