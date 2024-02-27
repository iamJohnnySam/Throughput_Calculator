import os
import tkinter as tk
from functools import partial

from gui.new_layout import LayoutEditor


class LayoutManager:
    def __init__(self, master):
        self.master = master

        self.manage_layouts_window = tk.Toplevel(self.master)
        self.manage_layouts_window.title("New Window")
        self.manage_layouts_window.geometry("600x300")

        title = "MANAGE LAYOUTS"
        self.manage_layouts_window.title(title)
        tk.Label(self.manage_layouts_window, text=title, font=("Calibri", 20)).pack()
        tk.Label(self.manage_layouts_window).pack()

        self.layouts_frame = tk.Frame(self.manage_layouts_window)
        self.layouts_frame.pack()
        self.load_layouts()

        tk.Button(self.manage_layouts_window, text="Close", command=self.manage_layouts_window.destroy).pack()

    def load_layouts(self):
        for widget in self.layouts_frame.winfo_children():
            widget.destroy()

        layout_options = os.listdir("layouts")
        for lay in layout_options:
            layout_frame = tk.Frame(self.layouts_frame)
            layout_frame.pack(padx=5, pady=5)
            tk.Label(layout_frame, text=lay, width=50).pack(side=tk.LEFT)
            tk.Button(layout_frame, text="Edit", width=10, command=partial(self.edit_layout, lay)).pack(side=tk.LEFT)
            tk.Button(layout_frame, text="Delete", width=10, command=partial(self.del_layout, lay)).pack(side=tk.LEFT)

    def del_layout(self, layout: str):
        try:
            os.remove(os.path.join("layouts", layout))
        except PermissionError:
            print("Permission Error")
        self.load_layouts()

    def edit_layout(self, layout: str):
        try:
            LayoutEditor(self.master, layout=layout)
        except PermissionError:
            print("Permission Error")
        self.manage_layouts_window.destroy()
