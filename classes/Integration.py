import dataclasses

@dataclasses.dataclass
class Integration:
    name: str
    displayName: str
    connected: bool
    legacyIntegration: bool
    disabledAutomatically: bool
    disabledByUser: bool
    inMainGuild: bool