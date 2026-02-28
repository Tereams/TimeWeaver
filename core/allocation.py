from dataclasses import dataclass
from datetime import date

@dataclass
class AllocationBlock:
    date: date
    task_name: str
    hours: float