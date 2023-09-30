import discord
from discord.ext.commands import Greedy
from Libs.utils import Embed, MessageConstants, format_greedy

from .enums import PunishmentEnum


def produce_info_embed(
    type: PunishmentEnum, members: Greedy[discord.Member], reason: str
) -> Embed:
    members_list = format_greedy([user.mention for user in members])
    type_to_word_list = ["Ban", "Unban", "Kick", "Timeout"]
    type_to_lowercase_word = [
        "banned",
        "unbanned",
        "kicked",
        "issued timeouts to user(s)",
    ]
    title = f"Issued {type_to_word_list[type.value]}"
    desc = f"Successfully {type_to_lowercase_word[type.value]} {members_list}"
    if type == PunishmentEnum.KICK:
        title = "Kicked User(s)"
    elif type == PunishmentEnum.TIMEOUT:
        title = "Issued Timeouts to User(s)"
        desc = f"Successfully {type_to_lowercase_word[3]} ({members_list})"

    embed = Embed(title=title)
    embed.description = desc
    embed.add_field(name="Reason", value=reason or MessageConstants.NO_REASON.value)
    return embed
