import json
import tkinter as tk
from pathlib import Path

from gui import GUI

path = Path("layouts")
if not path.exists():
    path.mkdir(parents=True)

    dictionary = {
        "Wet Robot": {
            "type": "robot",
            "area": "wet",
            "count": 1,
            "get_time": 15,
            "put_time": 15
        },
        "Dry Robot": {
            "type": "robot",
            "area": "dry",
            "count": 1,
            "get_time": 15,
            "put_time": 15
        },
        "Loading": {
            "type": "station",
            "process": "loading",
            "area": "wet",
            "time": 0,
            "capacity": 100000,
            "count": 1,
            "buffer": False,
            "attach": ""
        },
        "Dip Coat": {
            "type": "station",
            "process": "dip coat",
            "area": "wet",
            "time": 5,
            "capacity": 1,
            "count": 1,
            "buffer": False,
            "attach": ""
        },
        "Dip Drip": {
            "type": "station",
            "process": "dip drip",
            "area": "wet",
            "time": 5,
            "capacity": 1,
            "count": 1,
            "buffer": False,
            "attach": "Dip Coat"
        },
        "Wet Air Anneal": {
            "type": "station",
            "process": "air anneal",
            "area": "wet",
            "time": 95,
            "capacity": 1,
            "count": 1,
            "buffer": False,
            "attach": ""
        },
        "Dry Air Anneal": {
            "type": "station",
            "process": "air anneal",
            "area": "dry",
            "time": 95,
            "capacity": 1,
            "count": 3,
            "buffer": False,
            "attach": ""
        },
        "Rinse": {
            "type": "station",
            "process": "rinse",
            "area": "wet",
            "time": 10,
            "capacity": 1,
            "count": 1,
            "buffer": False,
            "attach": ""
        },
        "Rinse Drip": {
            "type": "station",
            "process": "rinse drip",
            "area": "wet",
            "time": 5,
            "capacity": 1,
            "count": 1,
            "buffer": False,
            "attach": "Rinse"
        },
        "Wet Vac Anneal": {
            "type": "station",
            "process": "vac anneal",
            "area": "wet",
            "time": 185,
            "capacity": 2,
            "count": 1,
            "buffer": False,
            "attach": ""
        },
        "Dry Vac Anneal": {
            "type": "station",
            "process": "vac anneal",
            "area": "dry",
            "time": 185,
            "capacity": 2,
            "count": 1,
            "buffer": False,
            "attach": ""
        },
        "Unloading": {
            "type": "station",
            "process": "unloading",
            "area": "dry",
            "time": 0,
            "capacity": 100000,
            "count": 1,
            "buffer": False,
            "attach": ""
        }
    }
    json_object = json.dumps(dictionary, indent=4)

    with open("layouts/test_file.json", "w") as outfile:
        outfile.write(json_object)

root = tk.Tk()
simulator = GUI(root)
root.mainloop()
