from typing import TypedDict


# maybe want a msgspec struct?????
class AntiPingSession(TypedDict):
    session_id: int
    enabled: bool
