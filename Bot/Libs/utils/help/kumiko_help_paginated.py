import contextlib
from typing import List, Mapping, Optional

from discord.ext import commands
from Libs.utils import Embed
from Libs.utils.pages import FieldPageSource, KumikoPages


class KumikoHelpPaginated(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__(
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.CooldownMapping.from_cooldown(
                    1, 3.0, commands.BucketType.user
                ),
                "aliases": ["commands"],
            }
        )

    async def send(self, **kwargs) -> None:
        """a shortcut to sending to get_destination"""
        await self.get_destination().send(**kwargs)

    async def help_embed(
        self, title: str, description: str, commands: List[commands.Command]
    ) -> None:
        """The default help embed builder

        Mainly used so we don't repeat ourselves when building help embeds

        Args:
            title (str): The title of the embed. Usually the name of the cog, group, etc
            description (str): The description of the embed. Usually the desc of the cog or group
            commands (List[commands.Command]): List of commands
        """
        filteredCommands = await self.filter_commands(commands)
        fieldSource = [
            (self.get_command_signature(command), command.help or "No help found...")
            for command in filteredCommands
        ]
        sources = FieldPageSource(
            entries=fieldSource,
            per_page=6,
            inline=True,
            clear_description=False,
            title=title or "No",
            description=description or "No help found...",
        )
        pages = KumikoPages(source=sources, ctx=self.context)
        await pages.start()

    async def send_bot_help(
        self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]
    ) -> None:
        """Generates the help embed when the default help command is called

        Args:
            mapping (Mapping[Optional[commands.Cog], List[commands.Command]]): Mapping of cogs to commands
        """
        ctx = self.context
        embed = Embed(title=f"{ctx.me.display_name} Help")
        embed.set_thumbnail(url=ctx.me.display_avatar)
        embed.description = f"{ctx.me.display_name} is a multipurpose bot built with freedom and choice in mind."
        usable = 0

        for (
            cog,
            cmds,
        ) in mapping.items():  # iterating through our mapping of cog: commands
            if filtered_commands := await self.filter_commands(cmds):
                # if no commands are usable in this category, we don't want to display it
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:  # getting attributes dependent on if a cog exists or not
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No"
                    description = "Commands with no category"

                embed.add_field(
                    name=f"{name} Category [{amount_commands}]", value=description
                )

        # embed.description = f"{len(ctx.commands)} commands | {usable} usable"

        await self.send(embed=embed)

    async def send_command_help(self, command: commands.Command) -> None:
        """Triggers when a `<prefix>help <command>` is called

        Args:
            command (commands.Command): The command to get help for
        """
        signature = self.get_command_signature(
            command
        )  # get_command_signature gets the signature of a command in <required> [optional]
        embed = Embed(title=signature, description=command.help or "No help found...")

        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        can_run = "No"
        # command.can_run to test if the cog is usable
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"

        embed.add_field(name="Usable", value=can_run)

        if command._buckets and (
            cooldown := command._buckets._cooldown
        ):  # use of internals to get the cooldown of the command
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )

        await self.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog) -> None:
        """Send the help command when a `<prefix>help <cog>` is called

        Args:
            cog (commands.Cog): The cog requested
        """
        title = cog.qualified_name or "No"
        await self.help_embed(
            title=f"{title} Category",
            description=cog.description,
            commands=cog.get_commands(),
        )

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.help_embed(
            title=title, description=group.help, commands=group.commands
        )
