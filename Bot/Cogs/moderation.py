from datetime import timedelta
from typing import Optional

import discord
from discord import PartialEmoji, app_commands
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.utils import Embed, MessageConstants, is_mod, parse_time_str


class Moderation(commands.Cog):
    """A set of fine-tuned moderation commands"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> PartialEmoji:
        return PartialEmoji.from_str("<:blobban:759935431847968788>")

    @commands.hybrid_group(name="mod")
    async def mod(self, ctx: commands.Context):
        """A set of fine-tuned moderation commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @is_mod()
    @mod.command(name="ban")
    @app_commands.describe(
        users="The users to ban",
        delete_days="The number of days to delete messages for",
        reason="The reason for the ban",
    )
    async def ban(
        self,
        ctx: commands.Context,
        users: commands.Greedy[discord.Member],
        delete_days: Optional[int] = 0,
        *,
        reason: Optional[str] = None,
    ) -> None:
        """Bans users

        Examples:
        `>mod ban @user1 @user2 @user3`
        Bans user1, user2, and user3

        `>mod ban @user1 7 spam`
        Bans user1 and deletes their messages from the last 7 days with the reason "spam"
        """
        ban_list = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        del_seconds = (
            delete_days * 86400 if delete_days is not None and delete_days <= 7 else 7
        )
        for members in users:
            await members.ban(delete_message_seconds=del_seconds, reason=reason)
        embed = Embed(title="Issued Ban", description=f"Successfully banned {ban_list}")
        embed.add_field(name="Reason", value=reason or MessageConstants.NO_REASON)
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="unban")
    @app_commands.describe(
        users="The users to unban", reason="The reason for the unban"
    )
    async def unban(
        self,
        ctx: commands.Context,
        users: commands.Greedy[discord.User],
        *,
        reason: Optional[str] = None,
    ) -> None:
        """Unbans users

        Examples:
        `>mod unban @user1 @user2 @user3`
        Unbans user1, user2, and user3

        `>mod unban @user1 issue resolved`
        Unbans user1 with the reason "issue resolved"
        """
        unban_list = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        for members in users:
            await ctx.guild.unban(user=members, reason=reason)  # type: ignore
        embed = Embed(
            title="Issued Unban", description=f"Successfully unbanned {unban_list}"
        )
        embed.add_field(name="Reason", value=reason or MessageConstants.NO_REASON)
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="kick")
    @app_commands.describe(users="The users to kick", reason="The reason for the kick")
    async def kick(
        self,
        ctx: commands.Context,
        users: commands.Greedy[discord.Member],
        *,
        reason: Optional[str] = None,
    ) -> None:
        """Kicks users

        Example:
        `>mod kick @user1`
        Kicks user1
        """
        kick_list = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        for members in users:
            await members.kick(reason=reason)
        embed = Embed(
            title="Kicked User(s)", description=f"Successfully kicked {kick_list}"
        )
        embed.add_field(name="Reason", value=reason or MessageConstants.NO_REASON)
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="mute")
    @app_commands.describe(
        users="The users to mute",
        duration="The duration to mute the user for. Defaults to 30m",
        reason="The reason for the mute",
    )
    async def mute(
        self,
        ctx: commands.Context,
        users: commands.Greedy[discord.Member],
        duration: Optional[str] = "30m",
        *,
        reason: Optional[str] = None,
    ) -> None:
        """Mutes users

        Examples:
        `>mod mute @user 30m`
        Mutes the user for 30 minutes

        `>mod mute @user 1h this user is a troll`
        Mutes the user for 1 hour with the reason "this user is a troll"

        `>mod mute @user @user2 4h`
        Mutes both users for 4 hours
        """
        mute_list = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        parsed_time = parse_time_str(duration if duration is not None else "30m")
        if parsed_time is not None and parsed_time > timedelta(days=28):
            parsed_time = parse_time_str("28d")
        for members in users:
            await members.timeout(parsed_time, reason=reason)
        embed = Embed(
            title="Muted User(s)", description=f"Successfully muted {mute_list}"
        )
        embed.add_field(name="Reason", value=reason or MessageConstants.NO_REASON)
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="unmute")
    @app_commands.describe(
        users="The users to unmute", reason="The reason for the unmute"
    )
    async def unmute(
        self,
        ctx: commands.Context,
        users: commands.Greedy[discord.Member],
        *,
        reason: Optional[str] = None,
    ) -> None:
        """Unmutes users

        Examples:
        `>mod unmute @user`
        Unmutes the user

        `>mod unmute @user @user2`
        Unmutes both users

        `>mod unmute @user "timeout expired"`
        Unmutes the user with the reason "timeout expired"
        """
        unmute_list = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        for members in users:
            await members.timeout(None, reason=reason)
        embed = Embed(
            title="Unmuted User(s)", description=f"Successfully unmuted {unmute_list}"
        )
        embed.add_field(name="Reason", value=reason or MessageConstants.NO_REASON)
        await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Moderation(bot))
