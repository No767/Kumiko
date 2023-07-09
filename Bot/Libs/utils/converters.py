from discord.ext import commands


class PrefixConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        user_id = ctx.bot.user.id
        if argument.startswith((f"<@{user_id}>", f"<@!{user_id}>")):
            raise commands.BadArgument("That is a reserved prefix already in use.")
        if len(argument) > 100:
            raise commands.BadArgument("That prefix is too long.")
        return argument
