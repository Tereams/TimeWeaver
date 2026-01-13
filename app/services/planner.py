from app.models.task import Task

def allocate_evenly(task: Task, daily_hours: float) -> int:
    """
    Return how many days are needed to finish the task.
    """
    if daily_hours <= 0:
        raise ValueError("daily_hours must be positive")

    days = task.total_hours / daily_hours
    return int(days) + (1 if days % 1 > 0 else 0)
