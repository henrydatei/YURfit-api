import dataclasses

@dataclasses.dataclass
class LevelingProgress:
    currentLevel: int
    currentXP: int
    currentLevelRequiredXP: int
    currentLevelColor: str
    currentLevelContrastColor: str
    nextLevel: int
    nextLevelProgressPercent: float
    nextLevelRequiredXP: int
    nextLevelContrastColor: str
    nextLevelColor: str