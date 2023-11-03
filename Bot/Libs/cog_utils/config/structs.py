from typing import TypedDict


class ReservedConfig(TypedDict):
    logs: bool
    local_economy: bool
    redirects: bool
    pins: bool


class ReservedLogConfig(TypedDict):
    channel_id: int
    mod: bool
    eco: bool
    redirects: bool
