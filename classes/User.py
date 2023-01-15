import dataclasses
from datetime import datetime
from typing import List

from . import LevelingProgress
from . import Goal
from . import Badge

@dataclasses.dataclass
class User:
    username: str
    name: str
    age: int
    birthdate: datetime
    customaryHeight: int
    customaryWeight: int
    metricHeight: int
    metricWeight: int
    metric_units: bool
    sex: int
    photoURL: str
    timezone: str
    totalXP: int
    rank: int
    levelingProcess: LevelingProgress.LevelingProgress
    uid: str
    userChallenges: List[str]
    last_modified: datetime
    dailyGoal: List[Goal.Goal]
    overrideDailyGoal: bool
    automatchEnabled: bool
    badges: List[Badge.Badge]
    isValid: bool
    bioAdjust: float
    createdAt: datetime
    
