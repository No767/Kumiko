from __future__ import annotations

from typing import Any, Dict, List

import discord
from discord.ext import menus

from ..embeds import Embed


class BasicListSource(menus.ListPageSource):
    """Basic list source for the paginator"""

    async def format_page(self, menu: menus.Menu, entries: List[Any]):
        """Formats the given page

        Args:
            menu (menus.Menu): What menu should be formatted
            entries (List[Any]): List of all of the entries

        Returns:
            _type_: _description_
        """
        embed = discord.Embed(
            description=f"This is number {entries}.", color=discord.Colour.random()
        )
        return embed


class EmbedListSource(menus.ListPageSource):
    """Source for taking contents of an Embed, and formatting them into a page"""

    async def format_page(self, menu, entries: Dict[str, Any]) -> discord.Embed:
        """Formatter for the embed list source

        Ideally the structure of the entries should be:
        {
            "title": "Title of the embed",
            "description": "Description of the embed",
            "image": "Image of the embed",
            "thumbnail": "Thumbnail of the embed",
            [
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
        embed = Embed(
            title=entries["title"] if entries["title"] is not None else None,
            description=entries["description"]
            if entries["description"] is not None
            else None,
        )
        embed.set_image(url=entries["image"] if entries["image"] is not None else None)
        embed.set_thumbnail(
            url=entries["thumbnail"] if entries["thumbnail"] is not None else None
        )
        embed.set_footer(
            text=f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)"
        )
        if entries["fields"] is not None:
            for item in entries["fields"]:
                for k, v in item.items():
                    embed.add_field(name=k, value=v)
        return embed
