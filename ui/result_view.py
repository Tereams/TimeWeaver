import tkinter as tk
from app.models.daily_plan import DailyPlan
from collections import defaultdict
from app.models.allocation import AllocationBlock


class ResultView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="Daily Plan", font=("Arial", 12, "bold"))
        title.pack(anchor="w", pady=(0, 5))

        self.listbox = tk.Listbox(self, height=8)
        self.listbox.pack(fill="both", expand=True)

    def show_plan(self, plan: list[DailyPlan]):
        self.clear()

        for day in plan:
            self.listbox.insert(
                tk.END,
                f"{day.date.isoformat()}  |  {day.hours:.1f} h"
            )

    def clear(self):
        self.listbox.delete(0, tk.END)

    def show_allocations(self, allocations: list[AllocationBlock]):
        self.clear()

        grouped = defaultdict(list)

        for a in allocations:
            grouped[a.date].append(a)

        for d in sorted(grouped):
            total = sum(x.hours for x in grouped[d])
            self.listbox.insert(tk.END, f"{d.isoformat()}  |  total {total:.1f}h")

            for x in grouped[d]:
                self.listbox.insert(
                    tk.END,
                    f"   {x.task_name}: {x.hours:.1f}h"
                )
        
