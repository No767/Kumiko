from typing import Union

from attrs import define, field


@define
class LoggingGuildConfig:
    channel_id: Union[int, None]
    member_events: bool = field(default=True)
    mod_events: bool = field(default=True)
    eco_events: bool = field(default=False)


@define
class GuildConfig:
    id: int
    logging_config: Union[LoggingGuildConfig, None]
    logs: bool = field(default=True)
    birthday: bool = field(default=False)
    local_economy: bool = field(default=False)
    local_economy_name: str = field(default="Server Economy")
