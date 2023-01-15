import dataclasses

@dataclasses.dataclass
class Datapoint:
    position: int
    squats: float
    steps: int
    score: float
    xp: float
    calories: float
    time: int
    accumulatedXp: float = 0
    accumulatedCalories: float = 0
    accumulatedSteps: int = 0
    accumulatedSquats: float = 0
    accumulatedScore: float = 0
    accumulatedTime: int = 0
