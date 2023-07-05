import discord
from discord.utils import utcnow


class Embed(discord.Embed):
    """Kumiko's custom default embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 163, 253))
        super().__init__(**kwargs)


class SuccessActionEmbed(discord.Embed):
    """Kumiko's custom success action embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(75, 181, 67))
        kwargs.setdefault("title", "Action successful")
        kwargs.setdefault("description", "The action requested was successful")
        super().__init__(**kwargs)


class CancelledActionEmbed(discord.Embed):
    """Kumiko's custom confirm action embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 0, 51))
        kwargs.setdefault("title", "Action cancelled")
        kwargs.setdefault("description", "The action requested was cancelled")
        super().__init__(**kwargs)


class ErrorEmbed(discord.Embed):
    """Kumiko's custom error embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(214, 6, 6))
        kwargs.setdefault("title", "Oh no, an error has occurred!")
        kwargs.setdefault(
            "description",
            "Uh oh! It seems like the command ran into an issue! For support, please visit Kumiko's Support Server to get help!",
        )
        super().__init__(**kwargs)


class ConfirmEmbed(discord.Embed):
    """Kumiko's custom confirm embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 191, 0))
        kwargs.setdefault("title", "Are you sure?")
        super().__init__(**kwargs)


class JoinEmbed(discord.Embed):
    """Kumiko's custom join embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(127, 255, 0))
        kwargs.setdefault("timestamp", utcnow())
        super().__init__(**kwargs)


class LeaveEmbed(discord.Embed):
    """Kumiko's custom leave embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 0, 51))
        kwargs.setdefault("timestamp", utcnow())
        super().__init__(**kwargs)
