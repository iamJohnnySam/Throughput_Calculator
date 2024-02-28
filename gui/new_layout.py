import json
import os
import tkinter as tk
from functools import partial

import global_var


class LayoutEditor:
    def __init__(self, master, layout):
        self.layout_name = None
        self.current_layout: str = ""
        self.new_station_window = tk.Toplevel(master)
        self.new_station_window.title("New Window")
        self.new_station_window.geometry("1200x500")

        title = "CREATE LAYOUT"
        self.new_station_window.title(title)
        tk.Label(self.new_station_window, text=title, font=("Calibri", 20)).pack()

        self.main_frame = tk.Frame(self.new_station_window)
        self.main_frame.pack()

        self.breakdown_layout(layout)

    def breakdown_layout(self, layout: str = ""):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.current_layout = layout

        top_layout = tk.Frame(self.main_frame)
        top_layout.pack()
        stations_layout = tk.Frame(self.main_frame)
        stations_layout.pack(side=tk.LEFT)
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

        self.populate_stations(stations_layout)

    def populate_stations(self, top_layout: tk.Frame):
        for widget in top_layout.winfo_children():
            widget.destroy()

        f = open(os.path.join(global_var.layouts, self.current_layout))
        data: dict = json.load(f)

        layout = tk.Frame(top_layout)
        layout.pack()

        for station in data.keys():
            frame = tk.Frame(layout, highlightthickness=1, highlightbackground="black")
            frame.pack(padx=5, pady=5)

            small_width = 7

            tk.Label(frame, text="Name: ", width=small_width).pack(side=tk.LEFT)
            station_name = tk.Entry(frame, width=12)
            station_name.insert(0, station)
            station_name.pack(side=tk.LEFT)

            tk.Label(frame, text="Type: ", width=small_width).pack(side=tk.LEFT)
            tk.Label(frame, text=data[station]['type'], width=small_width).pack(side=tk.LEFT)

            tk.Label(frame, text="Area: ", width=small_width).pack(side=tk.LEFT)
            station_area = tk.Entry(frame, width=small_width)
            station_area.insert(0, data[station]['area'])
            station_area.pack(side=tk.LEFT)

            if data[station]['type'] == "robot":
                tk.Label(frame, text="Get Time: ", width=10).pack(side=tk.LEFT)
                station_get = tk.Entry(frame, width=10)
                station_get.insert(0, data[station]['get_time'])
                station_get.pack(side=tk.LEFT)

            elif data[station]['type'] == "station":
                tk.Label(frame, text="Process: ", width=10).pack(side=tk.LEFT)
                station_process = tk.Entry(frame, width=10)
                station_process.insert(0, data[station]['process'])
                station_process.pack(side=tk.LEFT)

            if data[station]['type'] == "robot":
                tk.Label(frame, text="Put Time: ", width=10).pack(side=tk.LEFT)
                station_put = tk.Entry(frame, width=small_width)
                station_put.insert(0, data[station]['put_time'])
                station_put.pack(side=tk.LEFT)

            elif data[station]['type'] == "station":
                tk.Label(frame, text="Time: ", width=10).pack(side=tk.LEFT)
                station_time = tk.Entry(frame, width=small_width)
                station_time.insert(0, data[station]['time'])
                station_time.pack(side=tk.LEFT)

            tk.Label(frame, text="Capacity: ", width=10).pack(side=tk.LEFT)
            if data[station]['type'] == "robot":
                tk.Label(frame, text="1", width=small_width).pack(side=tk.LEFT)

            elif data[station]['type'] == "station":
                station_capacity = tk.Entry(frame, width=10)
                station_capacity.insert(0, data[station]['capacity'])
                station_capacity.pack(side=tk.LEFT)

            tk.Label(frame, text="Count: ", width=small_width).pack(side=tk.LEFT)
            station_count = tk.Entry(frame, width=small_width)
            station_count.insert(0, data[station]['count'])
            station_count.pack(side=tk.LEFT)

            tk.Button(frame, text="\U00002B06", width=2).pack(side=tk.LEFT)
            tk.Button(frame, text="\U00002B07", width=2).pack(side=tk.LEFT)

        tk.Label(layout).pack()

        tk.Button(layout, text="Add Robot", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(layout, text="Add Station", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(layout, text="Add Buffer", width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(layout, text="Close", width=15, command=self.new_station_window.destroy).pack(side=tk.RIGHT, padx=5)
        tk.Button(layout, text="Save & Close", width=20, command=self.new_station_window.destroy).pack(side=tk.RIGHT,
                                                                                                       padx=5)

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
