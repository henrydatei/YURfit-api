import dataclasses
from datetime import datetime
from typing import List

from . import Tag

@dataclasses.dataclass
class Workout:
    startTime: datetime
    endTime: datetime
    calories: int
    gameId: str
    identifier: str
    duration: int
    squats: float
    steps: int
    xp: float
    clientVersion: int
    validity: int
    isOfflineWorkout: bool
    isWorkoutActive: bool
    workoutId: str
    lastModified: datetime
    sourceName: str
    tags: List[Tag.Tag]