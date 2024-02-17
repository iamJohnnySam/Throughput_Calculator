import tkinter as tk
from tkinter import ttk

import logging
from payload import Payload


class Station:
    def __init__(self, process,
                 station_raw, station_type,
                 time: int = 1,
                 area: str = "",
                 capacity: int = 1,
                 buffer: bool = False):

        self._process = process
        self.attached_station = None
        self.area = area
        self.type = station_type
        self.raw_name = station_raw
        self.complete = False

        self._process_time = 0
        self._gui_process_time = None
        self._blocked = False

        self._stock = list()
        self._capacity = capacity
        self._gui_capacity = None

        self._time = time * 60
        self._wait_start = False
        self._waiting_time = 0
        self._gui_l_wait = None
        self._l_wait = 0
        self.buffer = buffer

        self.process_visible = False

        self._gui = None
        self._gui_payloads = None
        self._gui_wait_time = None
        self.robot_frame = None
        self.process_frame = None
        self._gui_block = None

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
    def process(self):
        return self._process

    @property
    def available(self):
        stock = len(self.stock) < self._capacity
        return stock and not self._blocked

    @property
    def gui(self):
        return self._gui

    @gui.setter
    def gui(self, gui_ob: tk.Frame):
        self._gui = gui_ob
        tk.Label(self._gui, text=self.process).pack(padx=4)

        # Time Frame
        time_frame = tk.Frame(self._gui)
        time_frame.pack(padx=4)
        self._gui_process_time = tk.Button(time_frame,
                                           text="time: " + str(self._process_time),
                                           width=18,
                                           command=self.toggle_process_parameters)
        self._gui_process_time.pack(padx=4)

        # Process Items Frame
        self.process_frame = ttk.Frame(self._gui)
        self.process_frame.pack(padx=4)
        self._gui_capacity = tk.Label(self.process_frame, text=str(len(self.stock)))
        self._gui_wait_time = tk.Label(self.process_frame, text="Pending")
        self._gui_l_wait = tk.Label(self.process_frame, text="Pending")
        self._gui_block = tk.Label(self.process_frame, text="False")
        tk.Label(self.process_frame, text="Details").grid(row=0, column=0)
        tk.Label(self.process_frame, text="Hidden").grid(row=0, column=1)

        self._gui_payloads = tk.Frame(self._gui, height="10")
        self._gui_payloads.pack(padx=4)

    def toggle_process_parameters(self):
        if self.process_visible:
            self.process_visible = False
            for widget in self.process_frame.winfo_children():
                widget.grid_forget()
            tk.Label(self.process_frame, text="Details").grid(row=0, column=0)
            tk.Label(self.process_frame, text="Hidden").grid(row=0, column=1)

        else:
            self.process_visible = True
            for widget in self.process_frame.winfo_children():
                widget.grid_forget()
            self.fill_process_frame()

    def fill_process_frame(self):
        att = "No" if self.attached_station is None else self.attached_station.raw_name

        tk.Label(self.process_frame, text='Area =').grid(row=0)
        tk.Label(self.process_frame, text=self.area).grid(row=0, column=1)
        tk.Label(self.process_frame, text='Attached =').grid(row=1)
        tk.Label(self.process_frame, text=att).grid(row=1, column=1)
        tk.Label(self.process_frame, text='Capacity =').grid(row=3)
        self._gui_capacity.grid(row=3, column=1)
        tk.Label(self.process_frame, text='Waiting =').grid(row=4)
        self._gui_wait_time.grid(row=4, column=1)
        tk.Label(self.process_frame, text='Last_wait =').grid(row=5)
        self._gui_l_wait.grid(row=5, column=1)
        tk.Label(self.process_frame, text='Blocked =').grid(row=6)
        self._gui_block.grid(row=6, column=1)

    def robot_pickup(self, payload: Payload):
        self._stock.remove(payload)
        self._process_time = 0
        logging.log(f"{self._process} REMOVED {payload.payload_id}")
        self.update_gui_payloads()

        if self.attached_station is not None and len(self._stock) == 0:
            self.attached_station.blocked = False

    def robot_place(self, payload: Payload):
        self._wait_start = True
        self.complete = False
        self._process_time = 0
        self._stock.append(payload)
        logging.log(f"{self._process} RECEIVED {payload.payload_id}")
        self.update_gui_payloads()

        if self.attached_station is not None and len(self._stock) > 0:
            self.attached_station.blocked = True

    def robot_block(self, robot, unblock=False):
        if unblock:
            self._stock.remove(robot)
        else:
            self._stock.append(robot)
        self.update_gui_payloads()

    def update_gui_payloads(self):
        for widget in self._gui_payloads.winfo_children():
            widget.destroy()
        i = 0
        for payload in reversed(self._stock):
            i = i + 1
            if type(payload) is not Payload:
                tk.Label(self._gui_payloads, text=str(payload.robot_name), fg="blue").pack()
            else:
                tk.Label(self._gui_payloads, text="PAYLOAD " + str(payload.payload_id),
                         fg="green" if payload.waiting else "black").pack()
            if i >= 4:
                break
        self._gui_capacity["text"] = str(len(self._stock))
        self._gui_block["text"] = str(self._blocked)

    def run(self):
        contain_waiting_payload = False
        no_robots = True
        for payload in self._stock:
            if type(payload) is not Payload:
                no_robots = False
                continue
            contain_waiting_payload = contain_waiting_payload or payload.waiting

        if not self.available and no_robots and not self._blocked and not contain_waiting_payload and not self.complete:
            self._l_wait = 0
            self._process_time = self._process_time + 1

            self._gui_process_time["text"] = "time: " + str(self._time - self._process_time)
            self._gui_process_time["fg"] = 'red' if self._process_time >= self._time else 'black'

            if self._time <= self._process_time:
                self.complete = True
                for item in self._stock:
                    item.waiting = True
                self.update_gui_payloads()

        else:
            if self._wait_start:
                self._waiting_time = self._waiting_time + 1
                self._gui_wait_time["text"] = str(self._waiting_time)
                self._l_wait = self._l_wait + 1
                self._gui_l_wait["text"] = str(self._l_wait)

