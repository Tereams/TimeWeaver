from app.models.task import Task
from app.services.planner import generate_daily_plan


def test_generate_daily_plan():
    task = Task(name="Test", total_hours=10)

    plan = generate_daily_plan(task, daily_hours=3)

    assert len(plan) == 4
    assert plan[0].hours == 3
    assert plan[-1].hours == 1
