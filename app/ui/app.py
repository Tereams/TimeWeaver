import tkinter as tk
from tkinter import messagebox

from app.config import APP_TITLE, WINDOW_SIZE
from app.models.task import Task
from app.services.planner import allocate_evenly

from app.ui.task_input_view import TaskInputView
from app.ui.result_view import ResultView
from app.ui.task_list_view import TaskListView


class TaskPlannerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)

        self.tasks = []

        self._build_ui()

    def _build_ui(self):
        main = tk.Frame(self.root)
        main.pack(fill="both", expand=True)

        # ---- Left: Task list ----
        self.task_list = TaskListView(
            main,
            on_select_callback=self._on_task_selected
        )
        self.task_list.pack(side="left", fill="y", padx=10, pady=10)

        # ---- Right panel ----
        right = tk.Frame(main)
        right.pack(side="right", fill="both", expand=True, padx=10)

        self.task_input = TaskInputView(right)
        self.task_input.pack(fill="x", pady=5)

        self.button = tk.Button(
            right,
            text="Add / Update Task",
            command=self._on_add_task
        )
        self.button.pack(pady=10)

        self.result_view = ResultView(right)
        self.result_view.pack(fill="x")

    def _on_add_task(self):
        try:
            data = self.task_input.get_input()

            name = data["name"].strip()
            total_hours = float(data["total_hours"])
            daily_hours = float(data["daily_hours"])

            if not name:
                raise ValueError("Task name cannot be empty")

            task = Task(name=name, total_hours=total_hours)

            self.tasks.append((task, daily_hours))
            self.task_list.add_task(task)

            days = allocate_evenly(task, daily_hours)
            self.result_view.show_result(
                f"Task '{task.name}' needs {days} days"
            )

            self.task_input.clear()

        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def _on_task_selected(self, task: Task):
        for t, daily_hours in self.tasks:
            if t is task:
                self.task_input.set_input(
                    t.name,
                    t.total_hours,
                    daily_hours
                )
                days = allocate_evenly(t, daily_hours)
                self.result_view.show_result(
                    f"Task '{t.name}' needs {days} days"
                )
                break

    def run(self):
        self.root.mainloop()
