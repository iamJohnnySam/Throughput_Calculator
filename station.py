import tkinter as tk

import data
import logging
from payload import Payload


class Station:
    def __init__(self, station_id, time,
                 capacity: int = 1,
                 robot: bool = False,
                 buffer: bool = False,
                 attached_station: str = ""):

        self._gui_block = None
        self._station_id = station_id
        self._attached_station = attached_station

        self._process_time = 0
        self._gui_process_time = None
        self._blocked = False

        self._stock = list()
        self._capacity = capacity
        self._gui_capacity = None

        self._robot_needed = robot
        self._robot_release = not robot
        self._time = time * 60
        self._wait_start = False
        self._waiting_time = 0
        self._gui_l_wait = None
        self._l_wait = 0
        self.buffer = buffer

        self._gui = None
        self._gui_payloads = None
        self._gui_wait_time = None
        self.robot_frame = None

    @property
    def stock(self):
        return self._stock

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, val):
        self._blocked = val
        self.update_gui_payloads()

    @stock.setter
    def stock(self, value):
        self._stock = value

    @property
    def station_id(self):
        return self._station_id

    @property
    def available(self):
        stock = len(self.stock) < self._capacity
        return stock and not self._blocked

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

        if self._attached_station == "":
            att = "No"
        else:
            att = self._attached_station

        process_frame = tk.Frame(self._gui)
        process_frame.pack()
        tk.Label(process_frame, text='Attached =').grid(row=0)
        tk.Label(process_frame, text=att).grid(row=0, column=1)
        tk.Label(process_frame, text='Time =').grid(row=1)
        self._gui_process_time = tk.Label(process_frame, text=self._process_time)
        self._gui_process_time.grid(row=1, column=1)
        tk.Label(process_frame, text='Capacity =').grid(row=2)
        self._gui_capacity = tk.Label(process_frame, text=str(len(self.stock)))
        self._gui_capacity.grid(row=2, column=1)
        tk.Label(process_frame, text='Waiting =').grid(row=3)
        self._gui_wait_time = tk.Label(process_frame, text="Pending")
        self._gui_wait_time.grid(row=3, column=1)
        tk.Label(process_frame, text='Last_wait =').grid(row=4)
        self._gui_l_wait = tk.Label(process_frame, text="Pending")
        self._gui_l_wait.grid(row=4, column=1)
        tk.Label(process_frame, text='Blocked =').grid(row=5)
        self._gui_block = tk.Label(process_frame, text="False")
        self._gui_block.grid(row=5, column=1)

        tk.Label(self._gui).pack()

        self._gui_payloads = tk.Frame(self._gui, height="10")
        self._gui_payloads.pack()
        tk.Label(self._gui).pack()

    def robot_pickup(self, payload: Payload):
        self._stock.remove(payload)
        self._process_time = 0
        logging.log(f"{self._station_id} REMOVED {payload.payload_id}")
        self.update_gui_payloads()

        if self._attached_station != "" and len(self._stock) == 0:
            data.stations[self._attached_station].blocked = False

    def robot_place(self, payload: Payload):
        self._wait_start = True
        self._stock.append(payload)
        self._robot_release = False if self._robot_needed else True
        logging.log(f"{self._station_id} RECEIVED {payload.payload_id}")
        self.update_gui_payloads()

        if self._attached_station != "" and len(self._stock) > 0:
            data.stations[self._attached_station].blocked = True

    def update_gui_payloads(self):
        for widget in self._gui_payloads.winfo_children():
            widget.destroy()
        i = 0
        for payload in reversed(self._stock):
            i = i + 1
            tk.Label(self._gui_payloads, text="PAYLOAD " + str(payload.payload_id),
                     fg="green" if payload.waiting else "black").pack()
            if i >= 10:
                break
        self._gui_capacity["text"] = str(len(self._stock))
        self._gui_block["text"] = str(self._blocked)

    def run(self):
        cl = False
        for payload in self._stock:
            cl = cl or payload.waiting

        if not self.available and not self._blocked and not cl:
            self._l_wait = 0
            self._process_time = self._process_time + 1
            self._gui_process_time["text"] = self._time - self._process_time

            self._gui_process_time["fg"] = 'red' if self._process_time >= self._time else 'black'

            if self._time == self._process_time:
                self._robot_release = True
                for item in self._stock:
                    item.waiting = True
                self.update_gui_payloads()

        else:
            if self._wait_start:
                self._waiting_time = self._waiting_time + 1
                self._gui_wait_time["text"] = str(self._waiting_time)
                self._l_wait = self._l_wait + 1
                self._gui_l_wait["text"] = str(self._l_wait)
