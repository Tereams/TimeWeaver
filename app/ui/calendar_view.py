import tkinter as tk
from datetime import date
from app.models.daily_plan import DailyPlan
from collections import defaultdict
from app.models.allocation import AllocationBlock


class CalendarView(tk.Frame):
    WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(self, master):
        super().__init__(master)
        self.cells = {}
        self._build_ui()

    def _build_ui(self):
        # Header
        for col, day in enumerate(self.WEEKDAYS):
            tk.Label(
                self,
                text=day,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                width=12
            ).grid(row=0, column=col, sticky="nsew")

        # 6 rows to cover all weeks in a month
        for row in range(1, 7):
            for col in range(7):
                cell = tk.Label(
                    self,
                    text="",
                    borderwidth=1,
                    relief="solid",
                    width=12,
                    height=4,
                    anchor="nw",
                    justify="left"
                )
                cell.grid(row=row, column=col, sticky="nsew")
                self.cells[(row, col)] = cell

    def show_plan(self, plan: list[DailyPlan]):
        self.clear()
        if not plan:
            return

        # Find the Monday of the first week
        start = plan[0].date
        monday = start
        while monday.weekday() != 0:
            monday = monday.fromordinal(monday.toordinal() - 1)

        for dp in plan:
            delta_days = (dp.date - monday).days
            row = delta_days // 7 + 1
            col = dp.date.weekday()

            if (row, col) in self.cells:
                text = f"{dp.date.day}\n{dp.hours:.1f} h"
                self.cells[(row, col)].config(text=text)

    def clear(self):
        for cell in self.cells.values():
            cell.config(text="")

    def show_allocations(self, allocations: list[AllocationBlock]):
        self.clear()
        if not allocations:
            return

        grouped = defaultdict(list)

        for a in allocations:
            grouped[a.date].append(a)

        first_date = min(grouped)
        monday = first_date
        while monday.weekday() != 0:
            monday = monday.replace(day=monday.day - 1)

        for d, items in grouped.items():
            delta = (d - monday).days
            row = delta // 7 + 1
            col = d.weekday()

            total = sum(x.hours for x in items)

            text = f"{d.day}\n{total:.1f}h"

            names = [x.task_name for x in items][:2]

            if names:
                text += "\n" + ",".join(names)

            if (row, col) in self.cells:
                self.cells[(row, col)].config(text=text)