import dataclasses
from datetime import datetime

@dataclasses.dataclass
class FeedItem:
    lastModified: datetime
    title: str
    ownerUid: str
    createdAt: datetime
    date: datetime
    hideMainFeed: bool
    pictureUrl: str
    type: int # type = 0 is a game/workout, type = 1 is a challenge, type = 2 is an achievement
    activityId: str
    meta: dict # depends on type