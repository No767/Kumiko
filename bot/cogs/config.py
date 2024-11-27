from __future__ import annotations

from typing import TYPE_CHECKING, Union

import discord
from discord import app_commands
from discord.ext import commands
from libs.utils import Embed
from libs.utils.checks import is_manager
from libs.utils.prefix import get_prefix
from typing_extensions import Annotated

if TYPE_CHECKING:
    from libs.utils.context import GuildContext

    from bot.kumiko import Kumiko


class PrefixConverter(commands.Converter):
    async def convert(self, ctx: GuildContext, argument: str):
        user_id = ctx.bot.user.id  # type: ignore # Already logged in by this time
        if argument.startswith((f"<@{user_id}>", f"<@!{user_id}>", ">")):
            raise commands.BadArgument("That is a reserved prefix already in use.")
        if len(argument) > 100:
            raise commands.BadArgument("That prefix is too long.")
        return argument


class Config(commands.Cog):
    """Configuration layer for Kumiko"""

    def __init__(self, bot: Kumiko):
        self.bot = bot
        self.pool = self.bot.pool

    @property
    def display_emoji(self) -> discord.PartialEmoji:
        return discord.PartialEmoji(name="\U0001f6e0")

    ### Prefix utilities

    def clean_prefixes(self, prefixes: Union[str, list[str]]) -> str:
        if isinstance(prefixes, str):
            return f"`{prefixes}`"

        return ", ".join(f"`{prefix}`" for prefix in prefixes[2:])

    @is_manager()
    @commands.guild_only()
    @commands.hybrid_group(name="config")
    async def config(self, ctx: GuildContext) -> None:
        """Modifiable configuration layer for Kumiko"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @is_manager()
    @commands.guild_only()
    @config.group(name="prefix", fallback="info")
    async def prefix(self, ctx: GuildContext) -> None:
        """Shows and manages custom prefixes for the guild

        Passing in no subcommands will effectively show the currently set prefixes.
        """
        prefixes = await get_prefix(self.bot, ctx.message)
        embed = Embed()
        embed.add_field(
            name="Prefixes", value=self.clean_prefixes(prefixes), inline=False
        )
        embed.add_field(name="Total", value=len(prefixes) - 2, inline=False)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)  # type: ignore
        await ctx.send(embed=embed)

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="add")
    @app_commands.describe(prefix="The new prefix to add")
    async def prefix_add(
        self, ctx: GuildContext, prefix: Annotated[str, PrefixConverter]
    ) -> None:
        """Adds an custom prefix"""
        prefixes = await get_prefix(self.bot, ctx.message)

        # 2 are the mention prefixes, which are always prepended on the list of prefixes
        if isinstance(prefixes, list) and len(prefixes) > 13:
            await ctx.send(
                "You can not have more than 10 custom prefixes for your server"
            )
            return
        elif prefix in prefixes:
            await ctx.send("The prefix you want to set already exists")
            return

        query = """
            INSERT INTO guild_prefix (id, prefix) VALUES ($2, ARRAY[$1])
            ON CONFLICT (id) DO UPDATE
            SET prefix = ARRAY_APPEND(guild_prefix.prefix, $1) WHERE guild_prefix.id = $2;
        """
        await self.pool.execute(query, prefix, ctx.guild.id)
        get_prefix.cache_invalidate(self.bot, ctx.message)
        await ctx.send(f"Added prefix: `{prefix}`")

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="edit")
    @app_commands.describe(
        old="The prefix to edit", new="A new prefix to replace the old"
    )
    @app_commands.rename(old="old_prefix", new="new_prefix")
    async def prefix_edit(
        self,
        ctx: GuildContext,
        old: Annotated[str, PrefixConverter],
        new: Annotated[str, PrefixConverter],
    ) -> None:
        """Edits and replaces a prefix"""
        query = """
            UPDATE guild_prefix
            SET prefix = ARRAY_REPLACE(prefix, $1, $2)
            WHERE id = $3;
        """
        prefixes = await get_prefix(self.bot, ctx.message)

        guild_id = ctx.guild.id
        if old in prefixes:
            await self.pool.execute(query, old, new, guild_id)
            get_prefix.cache_invalidate(self.bot, ctx.message)
            await ctx.send(f"Prefix updated to from `{old}` to `{new}`")
        else:
            await ctx.send("The prefix is not in the list of prefixes for your server")

    @is_manager()
    @commands.guild_only()
    @prefix.command(name="delete")
    @app_commands.describe(prefix="The prefix to delete")
    async def prefix_delete(
        self, ctx: GuildContext, prefix: Annotated[str, PrefixConverter]
    ) -> None:
        """Deletes a set prefix"""
        query = "DELETE FROM guild_prefix WHERE id = $1;"
        msg = f"Do you want to delete the following prefix: {prefix}"
        confirm = await ctx.prompt(msg, timeout=120.0, delete_after=True)
        if confirm:
            await self.pool.execute(query, prefix, ctx.guild.id)
            get_prefix.cache_invalidate(self.bot, ctx.message)
            await ctx.send(f"The prefix `{prefix}` has been successfully deleted")
        elif confirm is None:
            await ctx.send("Confirmation timed out. Cancelled deletion...")
        else:
            await ctx.send("Confirmation cancelled. Please try again")


async def setup(bot: Kumiko) -> None:
    await bot.add_cog(Config(bot))
