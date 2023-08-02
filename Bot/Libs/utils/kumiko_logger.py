import logging
import re
from logging.handlers import RotatingFileHandler
from types import TracebackType
from typing import Optional, Type, TypeVar

import discord
from cysystemd import journal

from .utils import is_docker

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
        self.log = logging.getLogger()

    def __enter__(self) -> None:
        max_bytes = 32 * 1024 * 1024  # 32 MiB
        self.log.setLevel(logging.INFO)
        logging.getLogger("discord.ext.ipc.server").addFilter(RemoveIPCNoise())
        logging.getLogger("gql").setLevel(logging.WARNING)
        logging.getLogger("discord").setLevel(logging.INFO)
        handler = RotatingFileHandler(
            filename="kumiko.log",
            encoding="utf-8",
            mode="w",
            maxBytes=max_bytes,
            backupCount=5,
        )
        fmt = logging.Formatter(
            fmt="%(asctime)s %(levelname)s    %(message)s",
            datefmt="[%Y-%m-%d %H:%M:%S]",
        )
        handler.setFormatter(fmt)
        self.log.addHandler(handler)
        if not is_docker():
            self.log.addHandler(journal.JournaldLogHandler())
        discord.utils.setup_logging(formatter=fmt)

    def __exit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        handlers = self.log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            self.log.removeHandler(hdlr)
        # self.log.info("Shutting down Kumiko...")
