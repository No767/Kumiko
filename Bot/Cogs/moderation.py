from discord import PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.moderation import (
    BanFlags,
    KickFlags,
    PunishmentEnum,
    TimeoutFlags,
    UnbanFlags,
    produce_info_embed,
)
from Libs.utils import MessageConstants, is_mod


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
    async def ban(self, ctx: commands.Context, *, flags: BanFlags) -> None:
        """Bans users

        Examples:
        `>mod ban members: @user1 @user2 @user3`
        Bans user1, user2, and user3 with no reason attached

        `>mod ban members: @user1 delete_message: True reason: spammer`
        Bans user1 and deletes their messages with the reason "spammer"
        """
        del_seconds = 604800 if flags.delete_messages is True else 0  # 7 days
        for members in flags.members:
            await members.ban(delete_message_seconds=del_seconds, reason=flags.reason)
        embed = produce_info_embed(
            PunishmentEnum.BAN,
            flags.members,
            flags.reason or MessageConstants.NO_REASON.value,
        )
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="unban")
    async def unban(self, ctx: commands.Context, *, flags: UnbanFlags) -> None:
        """Unbans users

        Examples:
        `>mod unban members: @user1 @user2 @user3`
        Unbans user1, user2, and user3

        `>mod unban members: @user1 reason: issue resolved`
        Unbans user1 with the reason "issue resolved"
        """
        for members in flags.members:
            await ctx.guild.unban(user=members, reason=flags.reason)  # type: ignore

        embed = produce_info_embed(
            PunishmentEnum.UNBAN,
            flags.members,
            flags.reason or MessageConstants.NO_REASON.value,
        )
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="kick")
    async def kick(self, ctx: commands.Context, *, flags: KickFlags) -> None:
        """Kicks users

        Example:
        `>mod kick members: @user1`
        Kicks user1

        Example:
        `>mod kick members: @user1 resason: spammer`
        Kicks user1 with the reason of "spammer"
        """
        for user in flags.members:
            await user.kick(reason=flags.reason)
        embed = produce_info_embed(
            PunishmentEnum.KICK,
            flags.members,
            flags.reason or MessageConstants.NO_REASON.value,
        )
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="timeout", usage="members: @user")
    async def timeout(self, ctx: commands.Context, *, flags: TimeoutFlags) -> None:
        """Times out / Un-timeouts the given members

        Examples:
        `>mod timeout members: @user duration: 30m`
        Timeouts the user for 30 minutes

        `>mod timeout members: @user duration: 1h reason: this user is a troll`
        Mutes the user for 1 hour with the reason "this user is a troll"

        `>mod timeout members: @user @user2 4h`
        Mutes both users for 4 hours

        `>mod timeout members: @user reason: Good reason`
        Removes the timeout of @user with the reason of "Good Reason
        """
        dt = flags.duration

        for member in flags.members:
            await member.timeout(
                dt, reason=flags.reason or MessageConstants.NO_REASON.value  # type: ignore
            )

        embed = produce_info_embed(
            PunishmentEnum.TIMEOUT,
            flags.members,
            flags.reason or MessageConstants.NO_REASON.value,
        )
        await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Moderation(bot))
