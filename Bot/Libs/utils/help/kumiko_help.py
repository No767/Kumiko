import contextlib
from typing import List, Mapping, Optional

from discord.ext import commands
from Libs.utils import Embed


class KumikoHelp(commands.HelpCommand):
    def __init__(self):
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
            commands,
        ) in mapping.items():  # iterating through our mapping of cog: commands
            if filtered_commands := await self.filter_commands(commands):
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

    async def send_command_help(self, command):
        """triggers when a `<prefix>help <command>` is called"""
        signature = self.get_command_signature(
            command
        )  # get_command_signature gets the signature of a command in <required> [optional]
        embed = Embed(title=signature, description=command.brief or "No help found...")

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

    async def send_help_embed(
        self, title, description, commands
    ):  # a helper function to add commands to an embed
        embed = Embed(title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.help or "No help found...",
                )

        await self.send(embed=embed)

    async def send_group_help(self, group):
        """triggers when a `<prefix>help <group>` is called"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        """triggers when a `<prefix>help <cog>` is called"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(
            f"{title} Category", cog.description, cog.get_commands()
        )
