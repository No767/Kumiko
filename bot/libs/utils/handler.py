from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from bot.kumikocore import KumikoCore


class KeyboardInterruptHandler:
    def __init__(self, bot: KumikoCore):
        self.bot = bot
        self._task: Optional[asyncio.Task] = None

    def __call__(self):
        if self._task:
            raise KeyboardInterrupt
        self._task = self.bot.loop.create_task(self.bot.close())
