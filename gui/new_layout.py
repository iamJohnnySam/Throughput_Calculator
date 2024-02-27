import json
import os
import tkinter as tk
from functools import partial

import global_var


class LayoutEditor:
    def __init__(self, master, layout):
        self.layout_name = None
        self.current_layout: str = ""
        new_station_window = tk.Toplevel(master)
        new_station_window.title("New Window")
        new_station_window.geometry("800x500")

        title = "CREATE LAYOUT"
        new_station_window.title(title)
        tk.Label(new_station_window, text=title, font=("Calibri", 20)).pack()

        self.main_frame = tk.Frame(new_station_window)
        self.main_frame.pack()

        self.breakdown_layout(layout)

    def breakdown_layout(self, layout: str = ""):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_layout = layout

        top_layout = tk.Frame(self.main_frame)
        top_layout.pack()
        left_layout = tk.Frame(self.main_frame, width=self.main_frame.winfo_width() / 3)
        left_layout.pack(side=tk.LEFT, expand=True)
        right_layout = tk.Frame(self.main_frame, width=self.main_frame.winfo_width() * 2 / 3)
        right_layout.pack(side=tk.LEFT)
        bottom_layout = tk.Frame(self.main_frame)
        bottom_layout.pack()

        if self.current_layout == "":
            val = 0
            lay_path = os.path.join(global_var.layouts, f"LAYOUT_{val}.json")
            while os.path.isfile(lay_path):
                val = val + 1
                lay_path = os.path.join(global_var.layouts, f"LAYOUT_{val}.json")
            with open(lay_path, "w") as outfile:
                outfile.write(json.dumps({}, indent=4))
            self.current_layout = f"LAYOUT_{val}.json"

        tk.Label(top_layout, text="Layout Name:").pack(side=tk.LEFT)
        self.layout_name = tk.Entry(top_layout, width=50)
        self.layout_name.pack(side=tk.LEFT)
        self.layout_name.insert(0, self.current_layout)
        tk.Button(top_layout, text="Rename Layout",
                  command=partial(self.rename_layout, self.current_layout, self.layout_name.get())).pack(side=tk.LEFT)

        self.populate_stations(left_layout)

    def populate_stations(self, top_layout: tk.Frame):
        for widget in top_layout.winfo_children():
            widget.destroy()

        f = open(os.path.join(global_var.layouts, self.current_layout))
        data: dict = json.load(f)

        v = tk.Scrollbar(top_layout, orient='vertical')
        v.pack(side=tk.RIGHT, fill=tk.Y)

        layout = tk.Canvas(top_layout)
        layout.pack(expand=True, fill=tk.Y)
        v.config(command=layout.yview)

        for station in data.keys():
            frame = tk.Frame(layout, highlightthickness=1, highlightbackground="black")
            frame.pack(padx=5, pady=5)

            tk.Label(frame, text="Name: ").grid(row=0, column=0, padx=3)
            tk.Label(frame, text="Type: ").grid(row=0, column=2, padx=3)
            tk.Label(frame, text="Process: ").grid(row=1, column=0, padx=3)
            tk.Label(frame, text="Area: ").grid(row=1, column=2, padx=3)
            tk.Label(frame, text="Time: ").grid(row=2, column=0, padx=3)
            tk.Label(frame, text="Capacity: ").grid(row=2, column=2, padx=3)
            tk.Label(frame, text="Count: ").grid(row=3, column=0, padx=3)

            tk.Label(frame, text=station).grid(row=0, column=1, padx=3)
            tk.Label(frame, text=data[station]['type']).grid(row=0, column=3, padx=3)
            try:
                tk.Label(frame, text=data[station]['process']).grid(row=1, column=1, padx=3)
            except KeyError:
                tk.Label(frame, text='transfer').grid(row=1, column=1, padx=3)
            tk.Label(frame, text=data[station]['area']).grid(row=1, column=3, padx=3)
            try:
                tk.Label(frame, text=data[station]['time']).grid(row=2, column=1, padx=3)
            except KeyError:
                tk.Label(frame, text=f"{data[station]['get_time']} | {data[station]['put_time']}").grid(row=2, column=1,
                                                                                                        padx=3)
            try:
                tk.Label(frame, text=str(data[station]['capacity'])).grid(row=2, column=3, padx=3)
            except KeyError:
                tk.Label(frame, text="1").grid(row=2, column=3, padx=3)
            tk.Label(frame, text=str(data[station]['count'])).grid(row=3, column=1, padx=3)

            tk.Button(frame, text="\U00002B06").grid(row=3, column=2, padx=3)
            tk.Button(frame, text="\U00002B07").grid(row=3, column=3, padx=3)

        layout.config(scrollregion=(0,0,layout.tk.X,layout.tk.Y), yscrollcommand=v.set)

    def rename_layout(self, old_name: str, new_name: str):
        if not new_name.endswith(".json"):
            new_name = new_name + ".json"

        try:
            os.rename(os.path.join(global_var.layouts, old_name),
                      os.path.join(global_var.layouts, new_name))
        except PermissionError:
            print("Permission Error")
            self.layout_name.insert(0, self.current_layout)
            return

        self.breakdown_layout(new_name)
