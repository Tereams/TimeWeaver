import tkinter as tk


class ResultView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build_ui()

    def _build_ui(self):
        self.label = tk.Label(
            self,
            text="",
            font=("Arial", 12),
            fg="blue"
        )
        self.label.pack(anchor="w")

    def show_result(self, text: str):
        self.label.config(text=text)

    def clear(self):
        self.label.config(text="")
