from datetime import date, timedelta
from app.models.task import Task
from app.models.daily_plan import DailyPlan


def generate_daily_plan(
    task: Task,
    daily_hours,
    start_date: date,
    working_days: set[int] | None = None,
    skip_dates: set[date] | None = None,
    deadline: date | None = None
) -> list[DailyPlan]:
    """
    Generate a work plan with:
    - variable daily hours
    - working days rule
    - blackout dates (skip_dates)
    """

    if working_days is None:
        working_days = {0, 1, 2, 3, 4}

    if skip_dates is None:
        skip_dates = set()

    if isinstance(daily_hours, (int, float)):
        daily_hours_map = {d: float(daily_hours) for d in working_days}
    elif isinstance(daily_hours, dict):
        daily_hours_map = daily_hours
    else:
        raise ValueError("daily_hours must be float or dict[int, float]")

    remaining = task.total_hours
    current_date = start_date
    day_index = 1
    plan: list[DailyPlan] = []

    while remaining > 0:

        if deadline is not None and current_date > deadline:
            raise ValueError("Task cannot be completed before deadline.")

        weekday = current_date.weekday()
        is_working_day = weekday in working_days
        is_skipped = current_date in skip_dates

        if is_working_day and not is_skipped:
            hours_today = daily_hours_map.get(weekday, 0)

            if hours_today > 0:
                hours_today = min(hours_today, remaining)

                plan.append(
                    DailyPlan(
                        day_index=day_index,
                        date=current_date,
                        hours=hours_today
                    )
                )

                remaining -= hours_today
                day_index += 1

        current_date += timedelta(days=1)

    return plan
