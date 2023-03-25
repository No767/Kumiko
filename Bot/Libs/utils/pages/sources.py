from __future__ import annotations

from typing import Any, Dict, List

import discord
from discord.ext import menus


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

    async def format_page(
        self, menu: menus.Menu, entries: Dict[str, Any]
    ) -> discord.Embed:
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
            entries (List[Dict[str, Any]]) List of all of the entries to format

        Returns:
            discord.Embed: An embed with the formatted entries
        """
        embed = discord.Embed(
            title=entries["title"], description=entries["description"]
        )
        return embed
