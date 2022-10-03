import asyncio
import datetime
import os
import traceback
import uuid

import discord
import uvloop
from admin_logs_utils import KumikoAdminLogsUtils
from dateutil import parser
from dateutil.parser import ParserError
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from pytimeparse.timeparse import timeparse

load_dotenv()

POSTGRES_PASSWORD = os.getenv("Postgres_Password_Dev")
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP_Dev")
POSTGRES_USERNAME = os.getenv("Postgres_Username_Dev")
POSTGRES_PORT = os.getenv("Postgres_Port_Dev")
POSTGRES_AL_DATABASE = os.getenv("Postgres_Admin_Logs_Database")
AL_CONNECTION_URI = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_AL_DATABASE}"

alUtils = KumikoAdminLogsUtils(AL_CONNECTION_URI)

# TODO: Replace the exceptions with meaningful ones
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    admin = SlashCommandGroup("admin", "Admin commands", guild_ids=[970159505390325842])
    adminTimeout = admin.create_subgroup(
        "timeout", "Timeouts commands", guild_ids=[970159505390325842]
    )
    adminLogs = admin.create_subgroup(
        "logs", "Access admin logs", guild_ids=[970159505390325842]
    )

    @admin.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def banMembers(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to ban"),
        reason: Option(str, "The reason for the ban"),
    ):
        """Bans the requested user"""
        await user.ban(delete_message_days=7, reason=reason)
        await ctx.respond(f"Successfully banned {user.name}. Reason: {reason}")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @admin.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unbanMembers(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to unban"),
        reason: Option(str, "The reason for the unban"),
    ):
        """Un-bans the requested user"""
        await ctx.guild.unban(user=user, reason=reason)
        await ctx.respond(f"Successfully unbanned {user.name}. Reason: {reason}")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @admin.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kickUser(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to kick out of the server"),
        reason: Option(str, "The reason for why", required=False),
    ):
        """Kicks the requested user"""
        await alUtils.addALRow(
            uuid=str(uuid.uuid4()),
            guild_id=ctx.guild.id,
            action_user_id=ctx.author.id,
            user_affected_id=user.id,
            type_of_action="kick",
            reason=reason,
            date_issued=datetime.datetime.utcnow().isoformat(),
            duration=0,
            resolved=False,
        )
        await user.kick(reason=reason)
        await ctx.respond(f"Successfully kicked {user.name}. Reason: {reason}")

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @adminTimeout.command(name="date")
    @commands.has_permissions(moderate_members=True)
    async def timeoutDate(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to timeout"),
        datetime: Option(str, "The date and time of the timeout"),
        reason: Option(str, "The reason for the timeout"),
    ):
        """Timeouts the user for a specified date"""
        try:
            parsedDatetime = parser.parse(datetime)
            await user.timeout(until=parsedDatetime, reason=reason)
            await ctx.respond(
                f"The user {user.display_name} has been successfully timed out until {parsedDatetime}. Reason: {reason}"
            )
        except ParserError:
            await ctx.respond(
                "It seems like you probably have inputted the incorrect format for the datetime. Some examples of this include: `August 5, 2022 12:00`, `3-4-2022 13:30`, `2022-08-03 12:00 pm`"
            )

    @adminTimeout.command(name="duration")
    @commands.has_permissions(moderate_members=True)
    async def timeoutDuration(
        self,
        ctx,
        *,
        user: Option(discord.Member, "The user to timeout"),
        duration: Option(str, "The duration of the timeout"),
        reason: Option(str, "The reason for the timeout", required=False),
    ):
        """Timeouts the user for a specified amount of time"""
        try:
            parsedTime = timeparse(duration)
            timeoutDuration = datetime.timedelta(seconds=parsedTime)
            await user.timeout_for(duration=timeoutDuration, reason=reason)
            await ctx.respond(
                f"{user.display_name} has been successfully timed out for {timeoutDuration}. Reason: {reason}",
                ephemeral=True,
            )
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
        reason: Option(
            str, "The reason why the timeout should be removed", required=False
        ),
    ):
        """Removes the timeout from the user"""
        try:
            await user.remove_timeout(reason=reason)
            await ctx.respond(
                f"Timeout for {user.display_name} has been successfully removed. \nReason: {reason}",
                ephemeral=True,
            )
        except Exception as e:
            await ctx.respond(
                f"An error occured: {type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            )

    @adminLogs.command(name="view")
    @commands.has_permissions(moderate_members=True)
    async def viewLogs(
        self,
        ctx,
        *,
        type_of_action: Option(
            str,
            "The type of action to look up",
            choices=["Ban", "Unban", "Timeout", "Kick"],
        ),
    ):
        """Allows admins to view admin logs"""
        typeOfAction = type_of_action.lower()
        res = await alUtils.selAction(
            type_of_action=typeOfAction, guild_id=ctx.guild.id
        )
        mainPages = pages.Paginator(
            pages=[
                discord.Embed(description=dict(mainItems)["reason"])
                .add_field(
                    name="Issuer",
                    value=await self.bot.get_or_fetch_user(
                        dict(mainItems)["action_user_id"]
                    ),
                    inline=True,
                )
                .add_field(
                    name="Affected User",
                    value=await self.bot.get_or_fetch_user(
                        dict(mainItems)["user_affected_id"]
                    ),
                    inline=True,
                )
                .add_field(
                    name="Date Issued",
                    value=parser.isoparse(dict(mainItems)["date_issued"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    inline=True,
                )
                .add_field(
                    name="Duration", value=dict(mainItems)["duration"], inline=True
                )
                .add_field(
                    name="Resolved", value=dict(mainItems)["resolved"], inline=True
                )
                for mainItems in res
            ],
            loop_pages=True,
        )
        await mainPages.respond(ctx.interaction, ephemeral=False)


def setup(bot):
    bot.add_cog(Admin(bot))
