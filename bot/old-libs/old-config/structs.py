import msgspec


class LoggingGuildConfig(msgspec.Struct):
    mod: bool = True
    eco: bool = False
    redirects: bool = False


class GuildConfig(msgspec.Struct):
    logs: bool = True
    local_economy: bool = False
    pins: bool = True
    voice_summary: bool = False


class FullGuildConfig(msgspec.Struct):
    config: GuildConfig
    logging_config: LoggingGuildConfig
