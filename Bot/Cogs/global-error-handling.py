import asyncio

import discord
import uvloop
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.MissingPermissions):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = (
                f"You are missing the following permissions: {error.missing_perms}"
            )
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.BotMissingPermissions):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = f"{self.bot.user.name} is currently missing the following permissions: {error.missing_perms}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.MissingAnyRole):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = (
                f"You are missing the following roles: {error.missing_roles}"
            )
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)
        elif isinstance(error, commands.BotMissingAnyRole):
            embedVar = discord.Embed(
                color=discord.Color.from_rgb(226, 199, 255))
            embedVar.description = f"{self.bot.user.name} is currently missing the following roles: {error.missing_roles}"
            msg = await ctx.send(embed=embedVar, delete_after=10)
            await msg.delete(delay=10)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class everyonePingChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.mention_everyone:
            embedVar = discord.Embed()
            embedVar.description = (
                f"{message.author.mention}, you can't mention everyone..."
            )
            await message.channel.send(embed=embedVar)
            await message.channel.purge(limit=3)

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
    bot.add_cog(everyonePingChecker(bot))
