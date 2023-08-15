from discord.ext import commands


class PrefixConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        user_id = ctx.bot.user.id
        if argument.startswith((f"<@{user_id}>", f"<@!{user_id}>")):
            raise commands.BadArgument("That is a reserved prefix already in use.")
        if len(argument) > 100:
            raise commands.BadArgument("That prefix is too long.")
        return argument


class PinName(commands.clean_content):
    def __init__(self, *, lower: bool = False):
        self.lower: bool = lower
        super().__init__()

    async def convert(self, ctx: commands.Context, argument: str) -> str:
        converted = await super().convert(ctx, argument)
        lower = converted.lower().strip()

        if len(lower) > 100:
            raise commands.BadArgument("Tag name is a maximum of 100 characters.")

        first_word, _, _ = lower.partition(" ")

        # get tag command.
        root: commands.GroupMixin = ctx.bot.get_command("pins")
        if first_word in root.all_commands:
            raise commands.BadArgument("This tag name starts with a reserved word.")

        return converted.strip() if not self.lower else lower


class JobName(commands.clean_content):
    def __init__(self, *, lower: bool = False):
        self.lower: bool = lower
        super().__init__()

    async def convert(self, ctx: commands.Context, argument: str) -> str:
        converted = await super().convert(ctx, argument)
        lower = converted.lower().strip()

        if len(lower) > 100:
            raise commands.BadArgument("Job name is a maximum of 100 characters.")

        first_word, _, _ = lower.partition(" ")

        root: commands.GroupMixin = ctx.bot.get_command("jobs")
        if first_word in root.all_commands:
            raise commands.BadArgument("This Job name starts with a reserved word.")

        return converted.strip() if not self.lower else lower


class PinAllFlags(commands.FlagConverter):
    all: bool = commands.flag(
        default=False,
        description="Whether to dump all pins in that server",
        aliases=["a"],
    )


class CheckLegitUser(commands.clean_content):
    def __init__(self, *, lower: bool = False):
        self.lower: bool = lower
        super().__init__()

    async def convert(self, ctx: commands.Context, argument: str):
        converted = await super().convert(ctx, argument)
        user_id = int(converted)

        if ctx.guild is None:
            raise commands.BadArgument(
                "This is being used in a DM. Doesn't work that way"
            )

        member = ctx.guild.get_member(user_id)
        if member is None:
            raise commands.BadArgument("This user doesn't exist in this server")

        return member.id
