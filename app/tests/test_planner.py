from datetime import date
from app.models.task import Task
from app.services.planner import generate_daily_plan


def test_generate_daily_plan():
    task = Task(name="Test", total_hours=10)

    plan = generate_daily_plan(task, daily_hours=3)

    assert len(plan) == 4
    assert plan[0].hours == 3
    assert plan[-1].hours == 1
from datetime import date
from app.models.task import Task
from app.services.planner import generate_daily_plan


def test_generate_daily_plan_with_date():
    task = Task(name="Test", total_hours=5)
    start = date(2026, 2, 1)

    plan = generate_daily_plan(task, daily_hours=2, start_date=start)

    assert plan[0].date == date(2026, 2, 1)
    assert plan[1].date == date(2026, 2, 2)
    assert plan[-1].hours == 1
    

def test_skip_weekend():
    task = Task(name="Weekend Test", total_hours=4)
    start = date(2026, 2, 6)  # Friday

    plan = generate_daily_plan(task, daily_hours=2, start_date=start)

    assert plan[0].date.weekday() == 4  # Friday
    assert plan[1].date.weekday() == 0  # Monday
