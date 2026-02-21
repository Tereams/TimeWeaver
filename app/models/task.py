from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Task:
    name: str
    total_hours: float
    deadline: Optional[date] = None
    priority: int = 0  