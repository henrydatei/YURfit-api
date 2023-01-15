import dataclasses
from datetime import datetime
from typing import List

from . import Datapoint

@dataclasses.dataclass
class Winner:
    active: bool
    photoUrl: str
    needsUpdate: bool
    uid: str
    name: str
    currentProgress: Datapoint.Datapoint
    lastModified: datetime = dataclasses.field(init = True, default = None)
    progress: List[Datapoint.Datapoint] = dataclasses.field(init = True, default_factory = list)
    currentPeriod: Datapoint.Datapoint = dataclasses.field(init = True, default = None)
    lastWorkout: datetime = dataclasses.field(init = True, default = None)