import dataclasses
from datetime import datetime

@dataclasses.dataclass
class Tag:
    tag: str
    duration: int
    time: datetime
    samplesIncluded: int
    hmdDistanceTravelled: float
    avgHeartRate: float
    avgEstHeartRate: float
    squats: float
    calories: float
    avgBurnRate: float
    leftDistanceTravelled: float
    rightDistanceTravelled: float