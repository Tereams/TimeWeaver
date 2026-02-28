import tkinter as tk
from tkinter import messagebox

from datetime import date

from app.config import APP_TITLE, WINDOW_SIZE
from app.models.task import Task
from app.services.planner import generate_daily_plan
from app.services.scheduler import schedule_tasks

from app.ui.task_input_view import TaskInputView
from app.ui.result_view import ResultView
from app.ui.task_list_view import TaskListView
from app.ui.calendar_view import CalendarView


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
        
        self.view_mode = "list"

        self.toggle_button = tk.Button(
            right,
            text="Switch to Calendar View",
            command=self._toggle_view
        )
        self.toggle_button.pack(pady=5)

        self.result_view = ResultView(right)
        self.result_view.pack(fill="both", expand=True)

        self.calendar_view = CalendarView(right)

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
            start_date = date.fromisoformat(data["start_date"])
            
            plan = generate_daily_plan(task, daily_hours, start_date)
            self.result_view.show_plan(plan)
            self.calendar_view.show_plan(plan)

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
                plan = generate_daily_plan(t, daily_hours)
                self.result_view.show_plan(plan)
                self.calendar_view.show_plan(plan)
                break
  

    def _toggle_view(self):
        if self.view_mode == "list":
            self.result_view.pack_forget()
            self.calendar_view.pack(fill="both", expand=True)
            self.toggle_button.config(text="Switch to List View")
            self.view_mode = "calendar"
        else:
            self.calendar_view.pack_forget()
            self.result_view.pack(fill="both", expand=True)
            self.toggle_button.config(text="Switch to Calendar View")
            self.view_mode = "list"

    def _run_multi_schedule(self):

        if not self.tasks:
            return

        task_objects = [t for t, _ in self.tasks]

        start_date = date.today()

        allocations = schedule_tasks(
            task_objects,
            daily_hours=5,
            start_date=start_date
        )

        self.result_view.show_allocations(allocations)
        self.calendar_view.show_allocations(allocations)
            
    def run(self):
        self.root.mainloop()
