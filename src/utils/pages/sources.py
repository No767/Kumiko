from __future__ import annotations

from typing import TYPE_CHECKING, Any

from discord.ext import menus

if TYPE_CHECKING:
    import discord

    from utils.embeds import Embed

    from .paginator import KumikoPages


class SimplePageSource(menus.ListPageSource):
    # Any type is used because this is what menus.ListPageSource expects
    async def format_page(self, menu: KumikoPages, page: Any) -> discord.Embed | Embed:  # noqa: ANN401
        pages = [
            f"{index + 1}. {entry}"
            for index, entry in enumerate(page, start=menu.current_page * self.per_page)
        ]

        maximum = self.get_max_pages()
        if maximum > 1:
            footer = (
                f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)"
            )
            menu.embed.set_footer(text=footer)

        menu.embed.description = "\n".join(pages)
        return menu.embed
