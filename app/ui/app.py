import tkinter as tk
from tkinter import messagebox

from app.config import APP_TITLE, WINDOW_SIZE
from app.models.task import Task
from app.services.planner import allocate_evenly


class TaskPlannerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)

        self._build_ui()

    def _build_ui(self):
        # Title
        title = tk.Label(self.root, text="Task Planner v0.1", font=("Arial", 16))
        title.pack(pady=10)

        # ---- Task Name ----
        tk.Label(self.root, text="Task name").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        # ---- Total Hours ----
        tk.Label(self.root, text="Total hours").pack()
        self.total_hours_entry = tk.Entry(self.root)
        self.total_hours_entry.pack()

        # ---- Daily Hours ----
        tk.Label(self.root, text="Daily hours").pack()
        self.daily_hours_entry = tk.Entry(self.root)
        self.daily_hours_entry.pack()

        # ---- Button ----
        self.button = tk.Button(
            self.root,
            text="Calculate days needed",
            command=self._on_calculate
        )
        self.button.pack(pady=10)

        # ---- Result ----
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

    def _on_calculate(self):
        try:
            name = self.name_entry.get().strip()
            total_hours = float(self.total_hours_entry.get())
            daily_hours = float(self.daily_hours_entry.get())

            if not name:
                raise ValueError("Task name cannot be empty")

            task = Task(name=name, total_hours=total_hours)
            days = allocate_evenly(task, daily_hours)

            self.result_label.config(
                text=f"Task '{task.name}' needs {days} days"
            )

        except ValueError as e:
            messagebox.showerror("Input error", str(e))

    def run(self):
        self.root.mainloop()
