from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import asyncpg
from discord.ext import commands
from Libs.ui.commons import ConfirmationView
from redis.asyncio.connection import ConnectionPool

if TYPE_CHECKING:
    from Bot.kumikocore import KumikoCore


class KContext(commands.Context):
    """Subclassed `commands.Context` with some extra goodies"""

    bot: KumikoCore

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def pool(self) -> asyncpg.Pool:
        """Allows you to access the global asyncpg pool stored within the bot

        Returns:
            asyncpg.Pool: Asyncpg pool
        """
        return bot.pool

    @property
    def redis_pool(self) -> ConnectionPool:
        """Allows you to access the global redis pool stored within the bot

        Returns:
            ConnectionPool: Redis pool
        """
        return bot.redis_pool

    async def prompt(
        self,
        message: str,
        *,
        timeout: float = 60.0,
        delete_after: bool = True,
        author_id: Optional[int] = None,
    ) -> Optional[bool]:
        """Prompts the user with an interaction confirmation dialog

        Args:
            message (str): The message to show along with the prompt
            timeout (float, optional): How long to wait until returning. Defaults to 60.0.
            delete_after (bool, optional): Deletes the prompt afterwards. Defaults to True.
            author_id (Optional[int], optional): The member who should respond to the prompt. Defaults to the author.

        Returns:
            Optional[bool]: The response of the prompt

            - ``True`` if explicit confirm,

            - ``False`` if explicit deny,

            - ``None`` if deny due to timeout
        """
        author_id = author_id or self.author.id
        view = ConfirmationView(
            timeout=timeout,
            delete_after=delete_after,
            author_id=author_id,
        )
        view.message = await self.send(message, view=view, ephemeral=delete_after)
        await view.wait()
        return view.value
