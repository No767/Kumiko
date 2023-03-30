from datetime import timedelta
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from Libs.utils import Embed, parseTimeStr


class Moderation(commands.Cog):
    """A set of fine-tuned moderation commands"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_group(name="mod")
    async def mod(self, ctx: commands.Context):
        """A set of fine-tuned moderation commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @mod.command(name="ban")
    @app_commands.describe(
        users="The users to ban",
        delete_days="The number of days to delete messages for",
        reason="The reason for the ban",
    )
    @commands.has_permissions(ban_members=True)
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
        userBanList = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        deleteSeconds = (
            delete_days * 86400 if delete_days is not None and delete_days <= 7 else 7
        )
        for members in users:
            await members.ban(delete_message_seconds=deleteSeconds, reason=reason)
        embed = Embed(
            title="Issued Ban", description=f"Successfully banned {userBanList}"
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        await ctx.send(embed=embed)

    @mod.command(name="unban")
    @app_commands.describe(
        users="The users to unban", reason="The reason for the unban"
    )
    @commands.has_permissions(ban_members=True)
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
        unbanList = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        for members in users:
            await ctx.guild.unban(user=members, reason=reason)  # type: ignore
        embed = Embed(
            title="Issued Unban", description=f"Successfully unbanned {unbanList}"
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        await ctx.send(embed=embed)

    @mod.command(name="kick")
    @app_commands.describe(users="The users to kick", reason="The reason for the kick")
    @commands.has_permissions(kick_members=True)
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
        kickList = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        for members in users:
            await members.kick(reason=reason)
        embed = Embed(
            title="Kicked User(s)", description=f"Successfully kicked {kickList}"
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        await ctx.send(embed=embed)

    @mod.command(name="mute")
    @app_commands.describe(
        users="The users to mute",
        duration="The duration to mute the user for. Defaults to 30m",
        reason="The reason for the mute",
    )
    @commands.has_permissions(moderate_members=True)
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
        muteList = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        parsedTime = parseTimeStr(duration if duration is not None else "30m")
        if parsedTime is not None and parsedTime > timedelta(days=28):
            parsedTime = parseTimeStr("28d")
        else:
            parsedTime = parseTimeStr("28d")
        for members in users:
            await members.timeout(parsedTime, reason=reason)
        embed = Embed(
            title="Muted User(s)", description=f"Successfully muted {muteList}"
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        await ctx.send(embed=embed)

    @mod.command(name="unmute")
    @app_commands.describe(
        users="The users to unmute", reason="The reason for the unmute"
    )
    @commands.has_permissions(moderate_members=True)
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
        unmuteList = (
            ", ".join([user.mention for user in users]).rstrip(",")
            if len(users) > 1
            else users[0].mention
        )
        for members in users:
            await members.timeout(None, reason=reason)
        embed = Embed(
            title="Unmuted User(s)", description=f"Successfully unmuted {unmuteList}"
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderation(bot))
