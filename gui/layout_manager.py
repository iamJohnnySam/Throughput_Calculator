import os
import tkinter as tk
from functools import partial


class LayoutManager:
    def __init__(self, master):
        manage_layouts_window = tk.Toplevel(master)
        manage_layouts_window.title("New Window")
        manage_layouts_window.geometry("600x300")

        title = "MANAGE LAYOUTS"
        manage_layouts_window.title(title)
        tk.Label(manage_layouts_window, text=title, font=("Calibri", 20)).pack()
        tk.Label(manage_layouts_window).pack()

        self.layouts_frame = tk.Frame(manage_layouts_window)
        self.layouts_frame.pack()
        self.load_layouts()

    def load_layouts(self):
        for widget in self.layouts_frame.winfo_children():
            widget.destroy()

        layout_options = os.listdir("layouts")
        for lay in layout_options:
            layout_frame = tk.Frame(self.layouts_frame)
            layout_frame.pack(padx=5, pady=5)
            tk.Label(layout_frame, text=lay, width=50).pack(side=tk.LEFT)
            tk.Button(layout_frame, text="Edit", width=10).pack(side=tk.LEFT)
            tk.Button(layout_frame, text="Delete", width=10, command=partial(self.del_layout, lay)).pack(side=tk.LEFT)

    def del_layout(self, layout: str):
        os.remove(os.path.join("layouts", layout))
        self.load_layouts()
