import inspect
import itertools
from typing import Any, Optional, Union

import discord
from discord.ext import commands, menus

from .pages import KumikoPages

# RGB Colors:
# Pink (255, 161, 231) - Used for the main bot page
# Lavender (197, 184, 255) - Used for cog and group pages
# Light Orange (255, 199, 184) - Used for command pages


def process_perms_name(
    command: Union[commands.Group, commands.Command],
) -> Optional[str]:
    merge_list = []
    if (
        all(isinstance(parent, commands.Group) for parent in command.parents)
        and len(command.parents) > 0
    ):
        # See https://stackoverflow.com/a/27638751
        merge_list = [
            next(iter(parent.extras["permissions"])) for parent in command.parents
        ]

    if "permissions" in command.extras:
        merge_list.extend([*command.extras["permissions"]])

    perms_set = sorted(set(merge_list))
    if len(perms_set) == 0:
        return None
    return ", ".join(name.replace("_", " ").title() for name in perms_set)


class GroupHelpPageSource(menus.ListPageSource):
    def __init__(
        self,
        group: Union[commands.Group, commands.Cog],
        entries: list[commands.Command],
        *,
        prefix: str,
    ):
        super().__init__(entries=entries, per_page=6)
        self.group: Union[commands.Group, commands.Cog] = group
        self.prefix: str = prefix
        self.title: str = f"{self.group.qualified_name} Commands"
        self.description: str = self.group.description

    def _process_description(self, group: Union[commands.Group, commands.Cog]):
        if isinstance(group, commands.Group) and "permissions" in group.extras:
            return f"{self.description}\n\n**Required Permissions**: {process_perms_name(group)}"
        return self.description

    async def format_page(self, menu: KumikoPages, commands: list[commands.Command]):
        embed = discord.Embed(
            title=self.title,
            description=self._process_description(self.group),
            colour=discord.Colour.from_rgb(197, 184, 255),
        )

        for command in commands:
            signature = f"{command.qualified_name} {command.signature}"
            embed.add_field(
                name=signature,
                value=command.short_doc or "No help given...",
                inline=False,
            )

        maximum = self.get_max_pages()
        if maximum > 1:
            embed.set_author(
                name=f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} commands)"
            )

        embed.set_footer(
            text=f'Use "{self.prefix}help command" for more info on a command.'
        )
        return embed


class HelpSelectMenu(discord.ui.Select["HelpMenu"]):
    def __init__(self, entries: dict[commands.Cog, list[commands.Command]], bot):
        super().__init__(
            placeholder="Select a category...",
            min_values=1,
            max_values=1,
            row=0,
        )
        self.cmds: dict[commands.Cog, list[commands.Command]] = entries
        self.bot = bot
        self.__fill_options()

    def __fill_options(self) -> None:
        self.add_option(
            label="Index",
            emoji="\N{WAVING HAND SIGN}",
            value="__index",
            description="The help page showing how to use the bot.",
        )
        for cog, cmds in self.cmds.items():
            if not cmds:
                continue
            description = cog.description.split("\n", 1)[0] or None
            emoji = getattr(cog, "display_emoji", None)
            self.add_option(
                label=cog.qualified_name,
                value=cog.qualified_name,
                description=description,
                emoji=emoji,
            )

    async def callback(self, interaction: discord.Interaction):
        if self.view is not None:
            value = self.values[0]
            if value == "__index":
                await self.view.rebind(FrontPageSource(), interaction)
            else:
                cog = self.bot.get_cog(value)
                if cog is None:
                    await interaction.response.send_message(
                        "Somehow this category does not exist?", ephemeral=True
                    )
                    return

                commands = self.cmds[cog]
                if not commands:
                    await interaction.response.send_message(
                        "This category has no commands for you", ephemeral=True
                    )
                    return

                source = GroupHelpPageSource(
                    cog, commands, prefix=self.view.ctx.clean_prefix
                )
                await self.view.rebind(source, interaction)


class HelpMenu(KumikoPages):
    def __init__(self, source: menus.PageSource, ctx: commands.Context):
        super().__init__(source, ctx=ctx, compact=True)

    def add_categories(
        self, commands: dict[commands.Cog, list[commands.Command]]
    ) -> None:
        self.clear_items()
        self.add_item(HelpSelectMenu(commands, self.ctx.bot))
        self.fill_items()

    async def rebind(
        self, source: menus.PageSource, interaction: discord.Interaction
    ) -> None:
        self.source = source
        self.current_page = 0

        await self.source._prepare_once()
        page = await self.source.get_page(0)
        kwargs = await self.get_kwargs_from_page(page)
        self._update_labels(0)
        await interaction.response.edit_message(**kwargs, view=self)


class FrontPageSource(menus.PageSource):
    def is_paginating(self) -> bool:
        # This forces the buttons to appear even in the front page
        return True

    def get_max_pages(self) -> Optional[int]:
        # There's only one actual page in the front page
        # However we need at least 2 to show all the buttons
        return 2

    async def get_page(self, page_number: int) -> Any:
        # The front page is a dummy
        self.index = page_number
        return self

    def format_page(self, menu: HelpMenu, page: Any):
        embed = discord.Embed(
            title="Bot Help", colour=discord.Colour.from_rgb(255, 161, 231)
        )
        embed.description = inspect.cleandoc(
            f"""
            Hello! Welcome to the help page.

            Use "{menu.ctx.clean_prefix}help command" for more info on a command.
            Use "{menu.ctx.clean_prefix}help category" for more info on a category.
            Use the dropdown menu below to select a category.
        """
        )
        
        embed.add_field(
            name="Support Server",
            value="For more help, consider joining the official server over at https://discord.gg/ns3e74frqn",
            inline=False,
        )

        if self.index == 0:
            embed.add_field(
                name="About Rodhaj",
                value=(
                    "Kumiko is an multipurpose bot that takes an unique and alternative approach to "
                    "what an multipurpose bot is. Kumiko offers features such as a redirects system, quiet mode, and many more. You can get more "
                    "information on the commands offered by using the dropdown below.\n\n"
                    "Kumiko is also open source. You can see the code on [GitHub](https://github.com/No767/Kumiko)"
                ),
                inline=False,
            )
        elif self.index == 1:
            entries = (
                ("<argument>", "This means the argument is __**required**__."),
                ("[argument]", "This means the argument is __**optional**__."),
                ("[A|B]", "This means that it can be __**either A or B**__."),
                (
                    "[argument...]",
                    "This means you can have multiple arguments.\n"
                    "Now that you know the basics, it should be noted that...\n"
                    "__**You do not type in the brackets!**__",
                ),
            )

            embed.add_field(
                name="How do I use this bot?",
                value="Reading the bot signature is pretty simple.",
            )

            for name, value in entries:
                embed.add_field(name=name, value=value, inline=False)

        return embed


class KumikoHelp(commands.HelpCommand):
    context: commands.Context

    def __init__(self):
        super().__init__(
            command_attrs={
                "cooldown": commands.CooldownMapping.from_cooldown(
                    1, 3.0, commands.BucketType.member
                ),
                "help": "Shows help about the bot, a command, or a category",
            }
        )

    async def on_help_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        if isinstance(error, commands.CommandInvokeError):
            # Ignore missing permission errors
            if (
                isinstance(error.original, discord.HTTPException)
                and error.original.code == 50013
            ):
                return

            await ctx.send(str(error.original))

    def get_command_signature(self, command: commands.Command) -> str:
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    async def send_bot_help(self, mapping):
        bot = self.context.bot

        def key(command) -> str:
            cog = command.cog
            return cog.qualified_name if cog else "\U0010ffff"

        entries: list[commands.Command] = await self.filter_commands(
            bot.commands, sort=True, key=key
        )

        all_commands: dict[commands.Cog, list[commands.Command]] = {}
        for name, children in itertools.groupby(entries, key=key):
            if name == "\U0010ffff":
                continue

            cog = bot.get_cog(name)
            if cog is not None:
                all_commands[cog] = sorted(children, key=lambda c: c.qualified_name)

        menu = HelpMenu(FrontPageSource(), ctx=self.context)
        menu.add_categories(all_commands)
        await menu.start()

    async def send_cog_help(self, cog):
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        menu = HelpMenu(
            GroupHelpPageSource(cog, entries, prefix=self.context.clean_prefix),
            ctx=self.context,
        )
        await menu.start()

    def common_command_formatting(
        self,
        embed_like: Union[discord.Embed, GroupHelpPageSource],
        command: commands.Command,
    ):
        embed_like.title = self.get_command_signature(command)
        processed_perms = process_perms_name(command)
        if isinstance(embed_like, discord.Embed) and processed_perms is not None:
            embed_like.add_field(name="Required Permissions", value=processed_perms)

        if command.description:
            embed_like.description = f"{command.description}\n\n{command.help}"
        else:
            embed_like.description = command.help or "No help found..."

    async def send_command_help(self, command):
        # No pagination necessary for a single command.
        embed = discord.Embed(colour=discord.Colour.from_rgb(255, 199, 184))
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        if len(entries) == 0:
            return await self.send_command_help(group)

        source = GroupHelpPageSource(group, entries, prefix=self.context.clean_prefix)
        self.common_command_formatting(source, group)
        menu = HelpMenu(source, ctx=self.context)
        await menu.start()