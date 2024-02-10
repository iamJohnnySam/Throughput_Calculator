import tkinter as tk

import data
import logging
from payload import Payload


class Station:
    def __init__(self, station_id, time, capacity: int = 1, robot: bool = False, process_input: bool = False,
                 process_output: bool = False,
                 waiting: bool = True,
                 buffer=False):

        self._station_id = station_id

        self._process_time = 0
        self._gui_process_time = None

        self._stock = list()
        self._capacity = capacity
        self._gui_capacity = None

        self._robot_needed = robot
        self._robot_release = not robot
        self._time = time * 60
        self.buffer = buffer

        self._gui = None
        self._gui_payloads = None
        self.robot_frame = None

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    @property
    def station_id(self):
        return self._station_id

    @property
    def available(self):
        return len(self.stock) < self._capacity

    @property
    def robot_needed(self):
        return self._robot_needed

    @property
    def robot_release(self):
        return self._robot_release

    @property
    def gui(self):
        return self._gui

    @gui.setter
    def gui(self, gui_ob):
        self._gui = gui_ob
        tk.Label(self._gui, text=self.station_id).pack()
        tk.Label(self._gui).pack()

        process_frame = tk.Frame(self._gui)
        process_frame.pack()
        tk.Label(process_frame, text='Time =').grid(row=0)
        self._gui_process_time = tk.Label(process_frame, text=self._process_time)
        self._gui_process_time.grid(row=0, column=1)
        tk.Label(process_frame, text='Capacity =').grid(row=1)
        self._gui_capacity = tk.Label(process_frame, text=str(len(self.stock)))
        self._gui_capacity.grid(row=1, column=1)
        tk.Label(self._gui).pack()

        self._gui_payloads = tk.Label(self._gui)
        self._gui_payloads.pack()
        tk.Label(self._gui).pack()

        self.robot_frame = tk.Frame(self._gui)
        self.robot_frame.pack()
        tk.Label(self._gui).pack()

    def robot_pickup(self, payload: Payload):
        self._stock.remove(payload)
        self._process_time = 0
        logging.log(f"{self._station_id} REMOVED {payload.payload_id}")
        self.update_gui_payloads()

    def robot_place(self, payload: Payload):
        self._stock.append(payload)
        self._robot_release = False if self._robot_needed else True
        logging.log(f"{self._station_id} RECEIVED {payload.payload_id}")
        self.update_gui_payloads()

    def update_gui_payloads(self):
        show_string = "- PAYLOADS -"
        for payload in self._stock:
            show_string = show_string + "\nPAYLOAD " + str(payload.payload_id)
        self._gui_payloads["text"] = show_string
        self._gui_capacity["text"] = str(len(self._stock))

    def run(self):
        if not self.available:
            self._process_time = self._process_time + 1
            self._gui_process_time["text"] = self._process_time
            if self._time > self._process_time:
                pass
            elif self._time == self._process_time:
                self._robot_release = True
                if not self._robot_needed:
                    for item in self._stock:
                        item.waiting = True
