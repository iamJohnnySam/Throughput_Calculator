import json
import os
import tkinter as tk
from functools import partial


class LayoutEditor:
    def __init__(self, master, layout):
        new_station_window = tk.Toplevel(master)
        new_station_window.title("New Window")
        new_station_window.geometry("500x500")

        title = "CREATE LAYOUT"
        new_station_window.title(title)
        tk.Label(new_station_window, text=title, font=("Calibri", 20)).pack()

        frame = tk.Frame(new_station_window)
        frame.pack()

        self.breakdown_layout(frame, layout)

    def breakdown_layout(self, window: tk.Frame, layout: str):
        top_layout = tk.Frame(window)
        top_layout.pack()
        left_layout = tk.Frame(window, width=window.winfo_width() / 3)
        left_layout.pack(side=tk.LEFT)
        right_layout = tk.Frame(window, width=window.winfo_width() * 2 / 3)
        right_layout.pack(side=tk.LEFT)
        bottom_layout = tk.Frame(window)
        bottom_layout.pack()

        if layout == "":
            val = 0
            lay_path = os.path.join("layouts", f"LAYOUT_{val}.json")
            while os.path.isfile(lay_path):
                val = val + 1
                lay_path = os.path.join("layouts", f"LAYOUT_{val}.json")
            f = open(lay_path, "w")
            path = lay_path
            layout = f"LAYOUT_{val}.json"
        else:
            path = os.path.join("layouts", layout)

        f = open(path)
        data = json.load(f)

        tk.Label(top_layout, text="Layout Name:").pack(side=tk.LEFT)
        layout_name = tk.Entry(top_layout, width=50)
        layout_name.pack(side=tk.LEFT)
        layout_name.insert(0, layout)
        tk.Button(top_layout, text="Rename Layout", command=partial(self.rename_layout, layout, layout_name.get()))

    def rename_layout(self, old_name, new_name):
        os.rename()