from dataclasses import dataclass
from datetime import date

@dataclass
class DailyPlan:
    day_index: int
    date: date
    hours: float
