from typing import Union

import discord
from Libs.utils import Embed, MessageConstants

from .enums import PunishmentEnum


def produce_info_embed(
    type: PunishmentEnum, member: Union[discord.Member, discord.User], reason: str
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
