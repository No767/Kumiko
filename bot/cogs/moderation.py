from typing import Union

import discord
from discord import Enum, PartialEmoji
from discord.ext import commands
from kumikocore import KumikoCore
from Libs.cog_utils.moderation.flags import BanFlags, KickFlags, TimeoutFlags
from Libs.utils import Embed, MessageConstants, is_mod


class PunishmentEnum(Enum):
    BAN = 0
    KICK = 2
    TIMEOUT = 3


class Moderation(commands.Cog):
    """A set of fine-tuned moderation commands"""

    def __init__(self, bot: KumikoCore) -> None:
        self.bot = bot

    def produce_info_embed(
        self,
        type: PunishmentEnum,
        member: Union[discord.Member, discord.User],
        reason: str,
    ) -> Embed:
        type_to_word_list = ["Ban", "Kick", "Timeout"]
        type_to_lowercase_word = [
            "banned",
            "kicked",
            "issued timeout to user",
        ]
        title = f"Issued {type_to_word_list[type.value]}"
        desc = f"Successfully {type_to_lowercase_word[type.value]} {member.global_name}"
        if type == PunishmentEnum.KICK:
            title = "Kicked User(s)"
        elif type == PunishmentEnum.TIMEOUT:
            title = "Issued Timeouts to User(s)"
            desc = f"Successfully {type_to_lowercase_word[3]} ({member.global_name})"

        embed = Embed(title=title)
        embed.description = desc
        embed.add_field(name="Reason", value=reason or MessageConstants.NO_REASON.value)
        return embed

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
        `>mod ban member: @user1`
        Bans user1 with no reason attached

        `>mod ban member: @user1 delete_message: True reason: spammer`
        Bans user1 and deletes their messages with the reason "spammer"
        """
        del_seconds = 604800 if flags.delete_messages is True else 0  # 7 days
        await flags.member.ban(delete_message_days=del_seconds, reason=flags.reason)
        embed = self.produce_info_embed(
            PunishmentEnum.BAN,
            flags.member,
            flags.reason or MessageConstants.NO_REASON.value,
        )
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="kick")
    async def kick(self, ctx: commands.Context, *, flags: KickFlags) -> None:
        """Kicks users

        Example:
        `>mod kick member: @user1`
        Kicks user1

        Example:
        `>mod kick member: @user1 resason: spammer`
        Kicks user1 with the reason of "spammer"
        """
        await flags.member.kick(reason=flags.reason)
        embed = self.produce_info_embed(
            PunishmentEnum.KICK,
            flags.member,
            flags.reason or MessageConstants.NO_REASON.value,
        )
        await ctx.send(embed=embed)

    @is_mod()
    @mod.command(name="timeout", usage="member: @user")
    async def timeout(self, ctx: commands.Context, *, flags: TimeoutFlags) -> None:
        """Times out / Un-timeouts the given members

        Examples:
        `>mod timeout member: @user duration: 30m`
        Timeouts the user for 30 minutes

        `>mod timeout member: @user duration: 1h reason: this user is a troll`
        Mutes the user for 1 hour with the reason "this user is a troll"
        """
        dt = flags.duration

        await flags.member.timeout(
            dt, reason=flags.reason or MessageConstants.NO_REASON.value  # type: ignore
        )

        embed = self.produce_info_embed(
            PunishmentEnum.TIMEOUT,
            flags.member,
            flags.reason or MessageConstants.NO_REASON.value,
        )
        await ctx.send(embed=embed)


async def setup(bot: KumikoCore) -> None:
    await bot.add_cog(Moderation(bot))
