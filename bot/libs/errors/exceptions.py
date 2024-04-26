from discord.ext.commands.errors import CheckFailure


class KumikoExceptionError(Exception):
    """Base exception class for Kumiko.

    Any exceptions can be ideally caught in this class, but is not recommended.
    """


class ValidationError(KumikoExceptionError):
    """Raised when a validation of any function fails"""


class EconomyDisabledError(CheckFailure):
    """Raised when the economy system is disabled in a guild"""

    def __init__(self) -> None:
        super().__init__(
            message="The economy module is disabled in this server. Please ask your server admin to enable it."
        )
        self.title = "Economy Disabled"


class RedirectsDisabledError(CheckFailure):
    """Raised when the redirects system is disabled in a guild"""

    def __init__(self) -> None:
        super().__init__(
            message="The redirects module is disabled in this server. Please ask your server admin to enable it."
        )
        self.title = "Redirects Disabled"


class PinsDisabledError(CheckFailure):
    """Raised when the pins system is disabled in a guild"""

    def __init__(self) -> None:
        super().__init__(
            message="The pins module is disabled in this server. Please ask your server admin to enable it."
        )
        self.title = "Pins Disabled"
