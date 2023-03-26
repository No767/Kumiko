import discord


class Embed(discord.Embed):
    """Kumiko's custom default embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 163, 253))
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
