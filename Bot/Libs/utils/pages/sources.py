from __future__ import annotations

from typing import Any, Dict

import discord
from discord.ext import menus

from ..embeds import Embed
from .paginator import KumikoPages


class EmbedListSource(menus.ListPageSource):
    """Source for taking contents of an Embed, and formatting them into a page"""

    async def format_page(
        self, menu: KumikoPages, entries: Dict[str, Any]
    ) -> discord.Embed:
        """Formatter for the embed list source

        Ideally the structure of the entries should be:
        {
            "title": "Title of the embed",
            "description": "Description of the embed",
            "image": "Image of the embed",
            "thumbnail": "Thumbnail of the embed",
            "fields": [
                {
                    "name": "Name of the embed",
                    "value": "Value of the embed",
                    "inline": True
                },
                {
                    "name": "Name of the embed",
                    "value": "Value of the embed",
                    "inline": True
                }
            ]
        }

        Args:
            menu (menus.Menu): What menu should be formatted
            entries (Dict[str, Any]) List of all of the entries to format

        Returns:
            discord.Embed: An embed with the formatted entries
        """
        maximum = self.get_max_pages()
        embed = Embed()
        embed.title = entries["title"] if "title" in entries else ""
        embed.description = entries["description"] if "description" in entries else ""
        embed.set_image(url=entries["image"]) if "image" in entries else ...
        embed.set_thumbnail(url=entries["thumbnail"]) if "thumbnail" in entries else ...
        embed.set_footer(text=f"Page {menu.current_page + 1}/{maximum}")
        if "fields" in entries:
            for item in entries["fields"]:
                embed.add_field(name=item["name"] or ..., value=item["value"] or ...)
        return embed


class SimplePageSource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        pages = []
        for index, entry in enumerate(entries, start=menu.current_page * self.per_page):
            pages.append(f"{index + 1}. {entry}")

        maximum = self.get_max_pages()
        if maximum > 1:
            footer = (
                f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)"
            )
            menu.embed.set_footer(text=footer)

        menu.embed.description = "\n".join(pages)
        return menu.embed
