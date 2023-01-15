import dataclasses
from datetime import datetime
from typing import List

@dataclasses.dataclass
class Period:
    index: int
    start: datetime
    end: datetime
    flags: int
    gameIds: List[int]
    calories: int = 0
    steps: int = 0