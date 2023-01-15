import dataclasses
from typing import List

@dataclasses.dataclass
class WorkoutSources:
    bidirectionalIntegrations: List[str]
    unidirectionalIntegrations: List[str]