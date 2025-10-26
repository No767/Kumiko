import logging
from logging.handlers import RotatingFileHandler
from types import TracebackType

from utils.checks import is_docker

MAX_BYTES = 32 * 1024 * 1024  # 32 MiB


class KumikoLogger:
    def __init__(self) -> None:
        self._disable_watchfiles_logger()

    def _get_formatter(self) -> logging.Formatter:
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        return logging.Formatter(
            "[{asctime}] [{levelname}]\t\t{message}", dt_fmt, style="{"
        )

    def _disable_watchfiles_logger(self) -> None:
        watchfiles = logging.getLogger("watchfiles")

        watchfiles.propagate = False
        watchfiles.addHandler(logging.NullHandler())

    def __enter__(self) -> None:
        discord_logger = logging.getLogger("discord")

        root = logging.getLogger("kumiko")

        handler = logging.StreamHandler()
        handler.setFormatter(self._get_formatter())

        if not is_docker():
            file_handler = RotatingFileHandler(
                filename="kumiko.log",
                encoding="utf-8",
                mode="w",
                maxBytes=MAX_BYTES,
                backupCount=5,
            )
            file_handler.setFormatter(self._get_formatter())

            discord_logger.addHandler(file_handler)
            root.addHandler(file_handler)

        discord_logger.setLevel(logging.INFO)
        discord_logger.addHandler(handler)

        root.setLevel(logging.INFO)
        root.addHandler(handler)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        root = logging.getLogger("kumiko")

        root.info("Shutting down...")
        handlers = root.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            root.removeHandler(hdlr)
