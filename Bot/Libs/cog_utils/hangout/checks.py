import discord
from discord.ext import commands

NOELLE_HANGOUT_HELP_CHANNEL_ID = 1145900494284402750


def check_if_thread(ctx: commands.Context):
    return (
        isinstance(ctx.channel, discord.Thread)
        and ctx.channel.parent_id == NOELLE_HANGOUT_HELP_CHANNEL_ID
    )


def is_help_thread():
    def pred(ctx: commands.Context):
        return check_if_thread(ctx)

    return commands.check(pred)
