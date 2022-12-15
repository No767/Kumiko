import asyncio
import logging
import os
import urllib.parse
from datetime import timedelta

import discord
import uvloop
from dateutil import parser
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands, pages
from dotenv import load_dotenv
from kumiko_admin_logs import KumikoAdminLogs, KumikoAdminLogsCacheUtils
from kumiko_servers import KumikoServerCacheUtils
from kumiko_ui_components import AdminLogsPurgeAllView
from kumiko_utils import KumikoCM
from pytimeparse.timeparse import timeparse
from rin_exceptions import NoItemsError

load_dotenv()

REDIS_HOST = os.getenv("Redis_Server_IP")
REDIS_PORT = os.getenv("Redis_Port")
POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("Postgres_Password"))
POSTGRES_SERVER_IP = os.getenv("Postgres_Server_IP")
POSTGRES_DATABASE = os.getenv("Postgres_Kumiko_Database")
POSTGRES_USERNAME = os.getenv("Postgres_Username")
POSTGRES_PORT = os.getenv("Postgres_Port")
CONNECTION_URI = f"asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER_IP}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
MODELS = ["kumiko_admin_logs.models", "kumiko_servers.models"]

cache = KumikoServerCacheUtils(
    uri=CONNECTION_URI, models=MODELS, redis_host=REDIS_HOST, redis_port=REDIS_PORT
)
cacheUtils = KumikoAdminLogsCacheUtils(
    uri=CONNECTION_URI, models=MODELS, redis_host=REDIS_HOST, redis_port=REDIS_PORT
)


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
        async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
            serverData = await cache.cacheServer(
                guild_id=ctx.guild.id, command_name=ctx.command.qualified_name
            )
            footerText = ""
            if serverData is None:
                logging.warning(
                    f"{ctx.guild.name} ({ctx.guild.id}) can't be found in the DB"
                )  # is logging really needed?
            elif int(serverData["admin_logs"] == False):
                footerText = "*Admin Logs are disabled for this server*"
            else:
                await KumikoAdminLogs.create(
                    guild_id=ctx.guild.id,
                    action="ban",
                    issuer=ctx.author.name,
                    affected_user=user.name,
                    reason=reason,
                    date_issued=discord.utils.utcnow().isoformat(),
                    duration=9999,
                )

            await user.ban(delete_message_seconds=3600, reason=reason)
            embed = discord.Embed(
                title=f"Banned {user.name}", color=discord.Color.from_rgb(255, 51, 51)
            )
            embed.description = (
                f"**Successfully banned {user.name}**\n\n**Reason:** {reason}"
            )
            embed.set_footer(text=footerText)
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
        async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
            serverData = await cache.cacheServer(
                guild_id=ctx.guild.id, command_name=ctx.command.qualified_name
            )
            footerText = ""
            if serverData is None:
                logging.warning(
                    f"{ctx.guild.name} ({ctx.guild.id}) can't be found in the DB"
                )  # is logging really needed?
            elif int(serverData["admin_logs"] == False):
                footerText = "*Admin Logs are disabled for this server*"
            else:
                await KumikoAdminLogs.create(
                    guild_id=ctx.guild.id,
                    action="unban",
                    issuer=ctx.author.name,
                    affected_user=user.name,
                    reason=reason,
                    date_issued=discord.utils.utcnow().isoformat(),
                    duration=9999,
                )

            await ctx.guild.unban(user=user, reason=reason)
            embed = discord.Embed(
                title=f"Unbanned {user.name}",
                color=discord.Color.from_rgb(178, 171, 255),
            )
            embed.description = (
                f"**Successfully unbanned {user.name}**\n\n**Reason:** {reason}"
            )
            embed.set_footer(text=footerText)
            await ctx.respond(embed=embed, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

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
        async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
            serverData = await cache.cacheServer(
                guild_id=ctx.guild.id, command_name=ctx.command.qualified_name
            )
            if serverData is None:
                logging.warning(
                    f"{ctx.guild.name} ({ctx.guild.id}) can't be found in the DB"
                )  # is logging really needed?
            elif int(serverData["admin_logs"] == False):
                pass
            else:
                await KumikoAdminLogs.create(
                    guild_id=ctx.guild.id,
                    action="kick",
                    issuer=ctx.author.name,
                    affected_user=user.name,
                    reason=reason,
                    date_issued=discord.utils.utcnow().isoformat(),
                    duration=0,
                )
            await user.kick(reason=reason)
            embed = discord.Embed(
                title=f"Kicked {user.name}", color=discord.Color.from_rgb(206, 255, 186)
            )
            embed.description = (
                f"**Successfully kicked {user.name}**\n\n**Reason:** {reason}"
            )
            await ctx.respond(embed=embed, ephemeral=True)

    # TODO: Tab selection for how long the user will be timed-out
    # This will be more than likely a modal
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
        async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
            try:
                serverData = await cache.cacheServer(
                    guild_id=ctx.guild.id, command_name=ctx.command.qualified_name
                )
                footerText = ""
                parsedTime = timeparse(duration)
                timeoutDuration = timedelta(seconds=parsedTime)
                if serverData is None:
                    logging.warning(
                        f"{ctx.guild.name} ({ctx.guild.id}) can't be found in the DB"
                    )  # is logging really needed?
                elif int(serverData["admin_logs"] == False):
                    footerText = "*Admin Logs are disabled for this server*"
                else:
                    await KumikoAdminLogs.create(
                        guild_id=ctx.guild.id,
                        action="timeout-duration",
                        issuer=ctx.author.name,
                        affected_user=user.name,
                        reason=reason,
                        date_issued=discord.utils.utcnow().isoformat(),
                        duration=timeoutDuration,
                    )
                await user.timeout_for(duration=timeoutDuration, reason=reason)
                embed = discord.Embed(
                    title=f"Timeout applied for {user.name}",
                    color=discord.Color.from_rgb(255, 255, 102),
                )
                embed.description = f"{user.name }has been successfully timed out for {timeoutDuration}\n\n**Reason:** {reason}"
                embed.set_footer(text=footerText)
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
        async with KumikoCM(uri=CONNECTION_URI, models=MODELS):
            serverData = await cache.cacheServer(
                guild_id=ctx.guild.id, command_name=ctx.command.qualified_name
            )
            footerText = ""
            if serverData is None:
                logging.warning(
                    f"{ctx.guild.name} ({ctx.guild.id}) can't be found in the DB"
                )  # is logging really needed?
            elif int(serverData["admin_logs"] == False):
                footerText = "*Admin Logs are disabled for this server*"
            else:
                await KumikoAdminLogs.create(
                    guild_id=ctx.guild.id,
                    action="timeout-remove",
                    issuer=ctx.author.name,
                    affected_user=user.name,
                    reason=reason,
                    date_issued=discord.utils.utcnow().isoformat(),
                    duration=0,
                )
            await user.remove_timeout(reason=reason)
            embed = discord.Embed(
                title=f"Timeout removed for {user.name}",
                color=discord.Color.from_rgb(255, 251, 194),
            )
            embed.description = f"Timeout for {user.name} has been successfully removed\n\n**Reason:** {reason}"
            embed.set_footer(text=footerText)
            await ctx.respond(embed=embed, ephemeral=True)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    @adminLogs.command(name="view")
    @commands.has_permissions(moderate_members=True)
    async def viewLogs(
        self,
        ctx,
        *,
        type_of_action: Option(
            str,
            "The type of action to look up",
            choices=[
                "All",
                "Ban",
                "Unban",
                "Kick",
                "Timeout-Remove",
                "Timeout-Duration",
            ],
        ),
    ):
        """Allows admins to view admin logs"""
        adminLogsData = await cacheUtils.cacheAdminLogsView(
            guild_id=ctx.guild.id,
            action=type_of_action.lower(),
            command_name=ctx.command.qualified_name,
        )
        try:
            if len(adminLogsData) == 0:
                raise NoItemsError
            else:
                mainPages = pages.Paginator(
                    pages=[
                        discord.Embed(
                            title=f"{item['type_of_action'].title()} - {item['affected_user']}",
                            description=item["reason"],
                        )
                        .add_field(name="Issuer", value=item["issuer"])
                        .add_field(name="Affected User", value=item["affected_user"])
                        .add_field(
                            name="Date Issued",
                            value=discord.utils.format_dt(
                                parser.isoparse(item["date_issued"])
                            ),
                        )
                        .add_field(name="Duration", value=item["duration"])
                        for item in adminLogsData
                    ],
                    loop_pages=True,
                )
                await mainPages.respond(ctx.interaction, ephemeral=True)
        except NoItemsError:
            embedErrorMessage = "Sorry, but either Admin Logs is disabled, or there are no logs found. Please try again."
            await ctx.respond(
                embed=discord.Embed(description=embedErrorMessage), ephemeral=True
            )

    @adminLogs.command(name="purge")
    @commands.has_permissions(moderate_members=True)
    async def purgeALData(self, ctx):
        """Purges all of the AL data for that guild (CAN'T BE UNDONE)"""
        embed = discord.Embed()
        embed.description = "Do you really wish to delete all of the AL data for this guild? This cannot be undone."
        view = AdminLogsPurgeAllView(
            uri=CONNECTION_URI,
            models=MODELS,
            redis_host=REDIS_HOST,
            redis_port=REDIS_PORT,
            command_name=ctx.command.qualified_name,
        )
        await ctx.respond(embed=embed, view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(Admin(bot))
