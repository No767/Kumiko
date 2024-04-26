from typing import List

import msgspec


class NekosImages(msgspec.Struct):
    id: str
    tags: List[str]
    created_at: str
