import discord
from discord.ext import commands


def check_if_thread(ctx: commands.Context):
    return isinstance(ctx.channel, discord.Thread) and not isinstance(
        ctx.channel, discord.ForumChannel
    )


def is_thread():
    def pred(ctx: commands.Context):
        return check_if_thread(ctx)

    return commands.check(pred)
