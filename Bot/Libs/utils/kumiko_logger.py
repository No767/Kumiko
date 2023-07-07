import logging
import re
from types import TracebackType
from typing import Optional, Type, TypeVar

import discord

BE = TypeVar("BE", bound=BaseException)


class RemoveIPCNoise(logging.Filter):
    def __init__(self) -> None:
        self.self = self

    def filter(self, record: logging.LogRecord) -> bool:
        matchRegex = r"(connection\s[open|closed])"
        if bool(re.search(matchRegex, record.msg)):
            return False
        return True


class KumikoLogger:
    def __init__(self) -> None:
        self.self = self
        self.log = logging.getLogger("discord")

    def __enter__(self) -> None:
        logging.getLogger("discord.ext.ipc.server").addFilter(RemoveIPCNoise())
        logging.getLogger("gql").setLevel(logging.WARNING)
        fmt = logging.Formatter(
            fmt="%(asctime)s %(levelname)s    %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]",
        )
        discord.utils.setup_logging(formatter=fmt)

    def __exit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        self.log.info("Shutting down Kumiko...")