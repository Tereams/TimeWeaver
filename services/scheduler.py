from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, List, Optional, Set, Union

from app.models.task import Task
from app.models.allocation import AllocationBlock


def _hours_for_weekday(
    daily_hours: Union[float, int, Dict[int, float]],
    weekday: int,
    working_days: Set[int],
) -> float:
    if isinstance(daily_hours, (int, float)):
        return float(daily_hours) if weekday in working_days else 0.0
    if isinstance(daily_hours, dict):
        return float(daily_hours.get(weekday, 0.0)) if weekday in working_days else 0.0
    raise ValueError("daily_hours must be float/int or dict[int, float]")


def _sort_key(task: Task):
    # deadline: None 
    # priority: -priority
    deadline_key = task.deadline if task.deadline is not None else date.max
    return (deadline_key, -task.priority, task.name)


@dataclass
class _WorkItem:
    task: Task
    remaining: float


def schedule_tasks(
    tasks: List[Task],
    daily_hours: Union[float, int, Dict[int, float]],
    start_date: date,
    working_days: Optional[Set[int]] = None,
    skip_dates: Optional[Set[date]] = None,
    hard_deadlines: bool = True,
) -> List[AllocationBlock]:
    """
    Multi-task scheduler:
    - Shared daily capacity (daily_hours)
    - Work only on working_days, skipping skip_dates
    - Greedy: earliest deadline first, then priority

    Returns: list of AllocationBlock(date, task_name, hours)
    """
    if working_days is None:
        working_days = {0, 1, 2, 3, 4}  # Mon-Fri
    if skip_dates is None:
        skip_dates = set()

    # Build work items
    items: List[_WorkItem] = []
    for t in tasks:
        if t.total_hours < 0:
            raise ValueError("task.total_hours must be >= 0")
        if t.total_hours == 0:
            continue
        items.append(_WorkItem(task=t, remaining=float(t.total_hours)))

    # Sort once; we will re-sort when items complete (cheap for v0.1)
    items.sort(key=lambda wi: _sort_key(wi.task))

    allocations: List[AllocationBlock] = []
    current = start_date

    # Safety: if there is zero capacity forever, we'd loop forever.
    # We'll detect "no usable days" in a rolling window.
    no_progress_days = 0

    while items:
        # Hard deadline check (before allocating on this date)
        if hard_deadlines:
            # If any task has deadline and we've moved past it while still remaining -> impossible
            for wi in items:
                if wi.task.deadline is not None and current > wi.task.deadline:
                    raise ValueError(f"Cannot complete '{wi.task.name}' before its deadline {wi.task.deadline.isoformat()}")

        if current in skip_dates:
            current += timedelta(days=1)
            continue

        weekday = current.weekday()
        capacity = _hours_for_weekday(daily_hours, weekday, working_days)

        if capacity <= 0:
            current += timedelta(days=1)
            no_progress_days += 1
            if no_progress_days > 14:
                raise ValueError("No schedulable capacity detected (check working_days/daily_hours/skip_dates).")
            continue

        no_progress_days = 0

        # Allocate today's capacity greedily across tasks
        remaining_capacity = capacity

        # Re-sort each day to reflect potential deadline pressure (still by same key)
        items.sort(key=lambda wi: _sort_key(wi.task))

        i = 0
        while i < len(items) and remaining_capacity > 0:
            wi = items[i]

            # If task has deadline and today is after deadline => caught above; if today is okay, proceed
            take = min(wi.remaining, remaining_capacity)
            if take > 0:
                allocations.append(
                    AllocationBlock(date=current, task_name=wi.task.name, hours=take)
                )
                wi.remaining -= take
                remaining_capacity -= take

            if wi.remaining <= 1e-9:
                items.pop(i)
                continue

            i += 1

        current += timedelta(days=1)

    return allocations