import datetime
import itertools
from typing import Optional, Union

import discord
import pygit2
from discord.ext import commands
from discord.utils import format_dt


def format_badges(ctx: commands.Context, user: Union[discord.Member, discord.User]):
    desc = ""
    badges_to_emoji = {
        "partner": "<:partnernew:754032603081998336>",  # Discord Bots
        "verified_bot_developer": "<:verifiedbotdev:853277205264859156>",  # Discord Bots
        "hypesquad_balance": "<:balance:585763004574859273>",  # Discord Bots
        "hypesquad_bravery": "<:bravery:585763004218343426>",  # Discord Bots
        "hypesquad_brilliance": "<:brilliance:585763004495298575>",  # Discord Bots
        "bug_hunter": "<:bughunter:585765206769139723>",  # Discord Bots
        "hypesquad": "<:hypesquad_events:585765895939424258>",  # Discord Bots
        "early_supporter": " <:supporter:585763690868113455> ",  # Discord Bots
        "bug_hunter_level_2": "<:goldbughunter:853274684337946648>",  # Discord Bots
        "staff": "<:staff_badge:1087023029105725481>",  # R. Danny
        "discord_certified_moderator": "<:certified_mod_badge:1087023030431129641>",  # R. Danny
        "active_developer": "<:active_developer:1087023031332900894>",  # R. Danny
    }

    set_flags = {flag for flag, value in user.public_flags if value}
    subset_flags = set_flags & badges_to_emoji.keys()
    badges = [badges_to_emoji[flag] for flag in subset_flags]

    if ctx.guild is not None and ctx.guild.owner_id == user.id:
        badges.append("<:owner:585789630800986114>")  # Discord Bots

    if (
        ctx.guild is not None
        and isinstance(user, discord.Member)
        and user.premium_since is not None
    ):
        badges.append("<:booster:1087022965775925288>")  # R. Danny

    if badges:
        desc = "".join(badges)

    return desc


def format_date(dt: Optional[datetime.datetime]):
    if dt is None:
        return "N/A"
    return f'{format_dt(dt, "F")} ({format_dt(dt, "R")})'


def format_commit(commit: pygit2.Commit) -> str:
    short, _, _ = commit.message.partition("\n")
    short_sha2 = commit.hex[0:6]
    commit_tz = datetime.timezone(datetime.timedelta(minutes=commit.commit_time_offset))
    commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(
        commit_tz
    )

    # [`hash`](url) message (offset)
    offset = format_dt(commit_time.astimezone(datetime.timezone.utc), "R")
    return f"[`{short_sha2}`](https://github.com/No767/Catherine-Chan/commit/{commit.hex}) {short} ({offset})"


def get_last_commits(count: int = 10):
    repo = pygit2.Repository(".git")
    commits = list(
        itertools.islice(
            repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count
        )
    )
    return "\n".join(format_commit(c) for c in commits)


def get_current_branch() -> str:
    repo = pygit2.Repository(".git")
    return repo.head.shorthand
