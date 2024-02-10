import tkinter as tk

import data
import logging
from payload import Payload


class Robot:
    def __init__(self, robot_id):
        self._gui_payloads = None
        self._gui = None
        self.next_station = ""
        self._robot_id = robot_id

        self._stock = []
        self._capacity = 1

        self._current_time = 0
        self._get_action = False
        self._put_action = False

        self._transfer_time = 15

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    @property
    def robot_id(self):
        return self._robot_id

    @property
    def available(self):
        return len(self.stock) < self._capacity

    @property
    def gui(self):
        return self._gui

    @gui.setter
    def gui(self, gui_ob):
        self._gui = gui_ob
        self._gui_payloads = tk.Label(self._gui)
        self._gui_payloads.pack()

    def pick(self, payload: Payload, next_station):
        payload.robot_pickup()
        self._stock.append(payload)
        self._current_time = 0
        self._get_action = True
        self._put_action = False
        self.next_station = next_station
        self.update_gui_payloads()

    def place(self, payload: Payload, next_station: str):
        logging.log(f"ROBOT {self._robot_id} PLACE INITIATED FOR PAYLOAD {payload.payload_id} TO {next_station}")
        data.stations[payload.current_station].robot_pickup(payload)
        payload.robot_pickup()
        self._current_time = 0
        self._get_action = False
        self._put_action = True
        payload.current_station = next_station
        self.update_gui_payloads()

    def update_gui_payloads(self):
        show_string = "- PAYLOADS -"
        for payload in self._stock:
            show_string = show_string + "\nPAYLOAD " + str(payload.payload_id)
        self._gui_payloads["text"] = show_string

    def run(self):
        if self._get_action:
            if self._current_time >= self._transfer_time:
                logging.log(f"ROBOT {self._robot_id} > RELEASED {self.stock[0].payload_id} "
                            f"FROM {self.stock[0].current_station}")
                self.place(self.stock[0], self.next_station)
                self._get_action = False

            if self._current_time == self._transfer_time:
                logging.log(f"ROBOT {self._robot_id} > PAYLOAD {self.stock[0].payload_id} "
                            f"AT {self.stock[0].current_station}")
                data.stations[self.stock[0].current_station].robot_pickup(self.stock[0])

            self._current_time = self._current_time + 1

        if self._put_action:
            if self._current_time < self._transfer_time:
                self._current_time = self._current_time + 1
            else:
                logging.log(f"ROBOT {self._robot_id} > PLACE ARRIVE {self.stock[0].payload_id} "
                            f"AT {self.stock[0].current_station}")
                self._put_action = False
                data.stations[self.stock[0].current_station].robot_place(self.stock[0])
                self._stock.remove(self.stock[0])
