import dataclasses
from datetime import datetime

@dataclasses.dataclass
class Badge:
    badgeTypeId: str
    badgeName: str
    badgeDescription: str
    badgeIconUrl: str
    badgeImageUrl: str
    badgeEarnedAt: datetime
    startTime: datetime
    endTime: datetime