import tkinter as tk
from tkinter import messagebox

from app.config import APP_TITLE, WINDOW_SIZE
from app.models.task import Task
from app.services.planner import allocate_evenly

from app.ui.task_input_view import TaskInputView
from app.ui.result_view import ResultView


class TaskPlannerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)

        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self.root, text="Task Planner v0.1", font=("Arial", 16))
        title.pack(pady=10)

        # ---- Task input ----
        self.task_input = TaskInputView(self.root)
        self.task_input.pack(padx=20, pady=10, fill="x")

        # ---- Action button ----
        self.button = tk.Button(
            self.root,
            text="Calculate days needed",
            command=self._on_calculate
        )
        self.button.pack(pady=10)

        # ---- Result view ----
        self.result_view = ResultView(self.root)
        self.result_view.pack(padx=20, pady=5, fill="x")

    def _on_calculate(self):
        try:
            data = self.task_input.get_input()

            name = data["name"].strip()
            total_hours = float(data["total_hours"])
            daily_hours = float(data["daily_hours"])

            if not name:
                raise ValueError("Task name cannot be empty")

            task = Task(name=name, total_hours=total_hours)
            days = allocate_evenly(task, daily_hours)

            self.result_view.show_result(
                f"Task '{task.name}' needs {days} days"
            )

        except ValueError as e:
            messagebox.showerror("Input error", str(e))
            self.result_view.clear()

    def run(self):
        self.root.mainloop()
