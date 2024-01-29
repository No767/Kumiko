from typing import TypedDict


class ReservedConfig(TypedDict):
    economy: bool
    redirects: bool
    voice_summary: bool


class ReservedLGC(TypedDict):
    mod: bool
    eco: bool
    redirects: bool
