import discord
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from discord.utils import format_dt


class Info(commands.Cog):
    """General info commands"""

    def __init__(self, bot):
        self.bot = bot

    info = SlashCommandGroup("info", "Gets the information needed of the bot")
    avatar = info.create_subgroup(
        "avatar",
        "Commands for getting discord user avatars",
    )

    @info.command(name="user")
    async def getUserInfo(
        self, ctx, *, user: Option(discord.Member, "The user to get the info of")
    ):
        """Gets info about the requested user"""
        embed = discord.Embed()
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.title = user.display_name
        embed.add_field(
            name="On Nitro Since (UTC)",
            value=format_dt(user.premium_since)
            if user.premium_since is not None
            else None,
            inline=True,
        )
        embed.add_field(
            name="Account Creation Date (UTC)",
            value=format_dt(user.created_at),
            inline=True,
        )
        embed.add_field(
            name="Server Join Date (UTC)",
            value=format_dt(user.joined_at) if user.joined_at is not None else None,
            inline=True,
        )
        embed.add_field(
            name="Timeout Since",
            value=format_dt(user.communication_disabled_until)
            if user.communication_disabled_until is not None
            else None,
            inline=True,
        )
        embed.add_field(
            name="Roles",
            value=str([roleName.name for roleName in user.roles][1:]).replace("'", ""),
            inline=True,
        )
        embed.add_field(name="Desktop Status", value=user.desktop_status, inline=True)
        embed.add_field(name="Web Status", value=user.web_status, inline=True)
        embed.add_field(name="On Mobile?", value=user.is_on_mobile(), inline=True)
        embed.add_field(name="Bot?", value=user.bot, inline=True)
        embed.add_field(name="Top Role", value=user.top_role.name, inline=True)
        embed.add_field(
            name="Mutual Guilds",
            value=str([guilds.name for guilds in user.mutual_guilds]).replace("'", ""),
            inline=True,
        )
        embed.add_field(name="Guild Nickname", value=user.nick, inline=True)
        embed.add_field(name="On Timeout?", value=user.timed_out, inline=True)
        await ctx.respond(embed=embed)

    @avatar.command(name="user")
    async def avatarGetUser(
        self, ctx, *, user: Option(discord.Member, "The username you wish to get")
    ):
        """Obtains the given user's avatar"""
        embed = discord.Embed()
        embed.title = f"{user.display_name}#{user.discriminator}'s avatar"
        embed.set_image(url=user.display_avatar.url)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
