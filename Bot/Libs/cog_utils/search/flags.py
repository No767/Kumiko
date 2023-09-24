from discord.ext import commands


class ModrinthFlags(commands.FlagConverter):
    query: str = commands.flag(
        aliases=["q"], description="The Minecraft project to search for"
    )
    project_type: str = commands.flag(
        default="mod",
        description="The category to filter out. Can be mod, plugin, etc. Defaults to mod",
    )
    loader: str = commands.flag(
        default="fabric",
        description="The loader to filter out. Examples include fabric, forge, spigot, etc. Defaults to fabric",
    )
    version: str = commands.flag(
        default="1.16.5",
        description="The version to filter out. Examples include 1.16.5, etc. Defaults to 1.16.5",
    )
