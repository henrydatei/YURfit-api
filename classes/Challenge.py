import dataclasses
from datetime import datetime
from typing import List

from . import Period
from . import Winner

@dataclasses.dataclass
class Challenge:
    challengeId: str
    name: str
    ownerUid: str
    permissionVisibility: int
    permissionInvite: int
    isStarted: bool
    isEnded: bool
    start: datetime
    end: datetime
    createdAt: datetime
    timezone: str
    minChallengers: int
    maxChallengers: int
    challengerCount: int
    periods: List[Period.Period]
    lastModified: datetime
    startedAt: datetime
    awaitChallenger: bool
    winners: List[Winner.Winner]
    imageUrl: str