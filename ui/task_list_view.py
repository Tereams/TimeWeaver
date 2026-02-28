import tkinter as tk


class TaskListView(tk.Frame):
    def __init__(self, master, on_select_callback):
        super().__init__(master)
        self.on_select_callback = on_select_callback
        self.tasks = []

        self._build_ui()

    def _build_ui(self):
        title = tk.Label(self, text="Tasks", font=("Arial", 12, "bold"))
        title.pack(anchor="w", pady=(0, 5))

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True)

        self.listbox.bind("<<ListboxSelect>>", self._on_select)

    def add_task(self, task):
        self.tasks.append(task)
        self.listbox.insert(tk.END, task.name)

    def _on_select(self, event):
        if not self.listbox.curselection():
            return
        index = self.listbox.curselection()[0]
        task = self.tasks[index]
        self.on_select_callback(task)
