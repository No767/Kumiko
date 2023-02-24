from datetime import timedelta

import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from pytimeparse.timeparse import timeparse


class Admin(commands.Cog):
    """A set of administrative commands"""

    def __init__(self, bot):
        self.bot = bot

    admin = SlashCommandGroup("admin", "Admin commands")
    adminTimeout = admin.create_subgroup("timeout", "Timeouts commands")
    adminLogs = admin.create_subgroup("logs", "Access admin logs")

    @admin.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def improvedBanMember(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to ban"),
        reason: Option(str, "The reason for the ban"),
    ):
        """Bans the requested user"""
        await user.ban(delete_message_seconds=3600, reason=reason)
        embed = discord.Embed(
            title=f"Banned {user.name}", color=discord.Color.from_rgb(255, 51, 51)
        )
        embed.description = (
            f"**Successfully banned {user.name}**\n\n**Reason:** {reason}"
        )
        await ctx.respond(embed=embed)

    @admin.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unbanMembers(
        self,
        ctx,
        *,
        user: Option(discord.User, "The user to unban"),
        reason: Option(str, "The reason for the unban"),
    ):
        """Un-bans the requested user"""
        await ctx.guild.unban(user=user, reason=reason)
        embed = discord.Embed(
            title=f"Unbanned {user.name}",
            color=discord.Color.from_rgb(178, 171, 255),
        )
        embed.description = (
            f"**Successfully unbanned {user.name}**\n\n**Reason:** {reason}"
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @admin.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kickUser(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to kick out of the server"),
        reason: Option(str, "The reason for why"),
    ):
        """Kicks the requested user"""
        await user.kick(reason=reason)
        embed = discord.Embed(
            title=f"Kicked {user.name}", color=discord.Color.from_rgb(206, 255, 186)
        )
        embed.description = (
            f"**Successfully kicked {user.name}**\n\n**Reason:** {reason}"
        )
        await ctx.respond(embed=embed, ephemeral=True)

    @adminTimeout.command(name="duration")
    @commands.has_permissions(moderate_members=True)
    async def timeoutDuration(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to timeout"),
        duration: Option(str, "The duration of the timeout"),
        reason: Option(str, "The reason for the timeout", default=None),
    ):
        """Applies a timeout to the user for a specified amount of time"""
        try:
            parsedTime = timeparse(duration)
            timeoutDuration = timedelta(seconds=parsedTime)
            await user.timeout_for(duration=timeoutDuration, reason=reason)
            embed = discord.Embed(
                title=f"Timeout applied for {user.name}",
                color=discord.Color.from_rgb(255, 255, 102),
            )
            embed.description = f"{user.name}has been successfully timed out for {timeoutDuration}\n\n**Reason:** {reason}"
            await ctx.respond(embed=embed, ephemeral=True)
        except TypeError:
            await ctx.respond(
                embed=discord.Embed(
                    description="It seems like you may have mistyped the amount of time for the timeout. Some examples that you can use are the following: `1h`, `1d`, `2 hours`, `5d`"
                )
            )

    @adminTimeout.command(name="remove")
    @commands.has_permissions(moderate_members=True)
    async def removeTimeout(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to remove the timeout from"),
        reason: Option(str, "The reason why the timeout should be removed"),
    ):
        """Removes the timeout from the user"""
        await user.remove_timeout(reason=reason)
        embed = discord.Embed(
            title=f"Timeout removed for {user.name}",
            color=discord.Color.from_rgb(255, 251, 194),
        )
        embed.description = f"Timeout for {user.name} has been successfully removed\n\n**Reason:** {reason}"
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Admin(bot))
