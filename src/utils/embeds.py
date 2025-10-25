import traceback

import discord


class Embed(discord.Embed):
    """Kumiko's custom default embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 163, 253))
        super().__init__(**kwargs)


class SuccessEmbed(discord.Embed):
    """Kumiko's custom success action embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(75, 181, 67))
        kwargs.setdefault("title", "Action successful")
        kwargs.setdefault("description", "The action requested was successful")
        super().__init__(**kwargs)


class ErrorEmbed(discord.Embed):
    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(214, 6, 6))
        kwargs.setdefault("title", "Oh no, an error has occurred!")
        kwargs.setdefault(
            "description",
            "Uh oh! It seems like the command ran into an issue! For support, ask the dev team",
        )
        super().__init__(**kwargs)


class FullErrorEmbed(ErrorEmbed):
    def __init__(self, error: Exception, **kwargs):
        kwargs.setdefault("description", self._format_description(error))
        super().__init__(**kwargs)

    def _format_description(self, error: Exception) -> str:
        error_traceback = "\n".join(traceback.format_exception_only(type(error), error))
        return f"""
        Uh oh! It seems like there was an issue. Ask the devs for help.

        **Error**:
        ```{error_traceback}```
        """


class CooldownEmbed(discord.Embed):
    def __init__(self, retry_after: float, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(214, 6, 6))
        kwargs.setdefault("timestamp", discord.utils.utcnow())
        kwargs.setdefault("title", "Command On Cooldown")
        kwargs.setdefault(
            "description",
            f"This command is on cooldown. Try again in {retry_after:.2f}s",
        )
        super().__init__(**kwargs)


class ConfirmEmbed(discord.Embed):
    """Kumiko's custom confirm embed"""

    def __init__(self, **kwargs):
        kwargs.setdefault("color", discord.Color.from_rgb(255, 191, 0))
        kwargs.setdefault("title", "Are you sure?")
        super().__init__(**kwargs)
