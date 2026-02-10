import tkinter as tk
import datetime


class TaskInputView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build_ui()

    def _build_ui(self):
        # ---- Task name ----
        tk.Label(self, text="Task name").pack(anchor="w")
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(fill="x")

        # ---- Total hours ----
        tk.Label(self, text="Total hours").pack(anchor="w", pady=(5, 0))
        self.total_hours_entry = tk.Entry(self)
        self.total_hours_entry.pack(fill="x")

        # ---- Daily hours ----
        tk.Label(self, text="Daily hours").pack(anchor="w", pady=(5, 0))
        self.daily_hours_entry = tk.Entry(self)
        self.daily_hours_entry.pack(fill="x")
        
        tk.Label(self, text="Start date (YYYY-MM-DD)").pack(anchor="w", pady=(5, 0))
        self.start_date_entry = tk.Entry(self)
        self.start_date_entry.pack(fill="x")
        self.start_date_entry.insert(0, datetime.date.today().isoformat())

    def get_input(self):
        """
        Return raw user input as strings.
        Validation is NOT done here.
        """
        return {
            "name": self.name_entry.get(),
            "total_hours": self.total_hours_entry.get(),
            "daily_hours": self.daily_hours_entry.get(),
        }

    def clear(self):
        self.name_entry.delete(0, tk.END)
        self.total_hours_entry.delete(0, tk.END)
        self.daily_hours_entry.delete(0, tk.END)
