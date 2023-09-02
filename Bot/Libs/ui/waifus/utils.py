import ciso8601
from discord.utils import format_dt
from yarl import URL

from .structs import NekosImages


class NekosImageEntry:
    __slots__ = ("id", "tags", "created_at")

    def __init__(self, entry: NekosImages):
        self.id = entry.id
        self.tags = entry.tags
        self.created_at = entry.created_at

    def to_dict(self):
        base_url = URL("https://nekos.moe")
        full_image_url = base_url / "image" / self.id
        post_url = base_url / "post" / self.id
        desc = (
            f"**Post URL**: {str(post_url)}\n"
            f"**Image URL**: {str(full_image_url)}.jpg\n"
            f"**Created At**: {format_dt(ciso8601.parse_datetime(self.created_at))}\n"
            f"**Tags**: {', '.join(self.tags).rstrip(',')}"
        )
        data = {"description": desc, "image": str(full_image_url)}
        return data
