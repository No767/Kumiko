from typing import Optional

from discord.ext.commands.errors import CommandError


class KumikoExceptionError(Exception):
    """Base exception class for Kumiko.

    Any exceptions can be ideally caught in this class, but is not recommended.
    """


class NoItemsError(KumikoExceptionError):
    """Raised when no items are found in a list.

    This is used when the JSON response from an API contains no items.
    """


class ItemNotFoundError(KumikoExceptionError):
    """Generally used if any item of the economy system is not found"""


class ValidationError(KumikoExceptionError):
    """Raised when a validation of any function fails"""


class HTTPError(KumikoExceptionError):
    """Raised when an HTTP request fails.

    This is used when the HTTP request to an API fails.

    Args:
        status (int): The status code of the HTTP request.
        message (Optional[str]): The message of the HTTP request.
    """

    def __init__(self, status: int, message: Optional[str]) -> None:
        self.status = status
        self.message = message
        fmt = self.message
        if message is None:
            fmt = f"HTTP request failed ({self.status})"
        super().__init__(fmt)


class NotFoundError(HTTPError):
    """Raised when an HTTP request fails with a 404 status code.

    This is used when the HTTP request to an API fails with a 404 status code.
    """

    def __init__(self) -> None:
        super().__init__(404, "Resource or endpoint not found")


class EconomyDisabledError(CommandError):
    """Raised when the economy system is disabled in a guild"""

    def __init__(self) -> None:
        super().__init__(
            message="The economy module is disabled in this server. Please ask your server admin to enable it."
        )


class RedirectsDisabledError(CommandError):
    """Raised when the redirects system is disabled in a guild"""

    def __init__(self) -> None:
        super().__init__(
            message="The redirects module is disabled in this server. Please ask your server admin to enable it."
        )


class PinsDisabledError(CommandError):
    """Raised when the pins system is disabled in a guild"""

    def __init__(self) -> None:
        super().__init__(
            message="The pins module is disabled in this server. Please ask your server admin to enable it."
        )
