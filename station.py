import json

import data
import logging
from payload import Payload


class Station:
    def __init__(self, station_id, time, capacity: int = 1, robot: bool = False, process_input: bool = False,
                 process_output: bool = False,
                 waiting: bool = True):

        self._robot_release = False
        self._station_id = station_id
        self._process_time = 0
        self._stock = list()
        self._capacity = capacity
        self._robot_needed = robot
        self._time = time

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        self._stock = value

    @property
    def available(self):
        return len(self.stock) < self._capacity

    @property
    def robot_needed(self):
        return self._robot_needed

    @property
    def robot_release(self):
        return self._robot_release

    def robot_pickup(self, payload: Payload):
        self._stock.remove(payload)
        self._process_time = 0
        logging.log(f"{self._station_id} REMOVED {payload.payload_id}")

    def robot_place(self, payload: Payload):
        self._stock.append(payload)
        self._robot_release = False if self._robot_needed else True
        logging.log(f"{self._station_id} RECEIVED {payload.payload_id}")

    def run(self):
        if not self.available:
            if self._time < self._process_time:
                self._process_time = self._process_time + 1
            else:
                self._robot_release = True
                if not self._robot_needed:
                    for item in self._stock:
                        item.waiting = True




"""
    def run(self, time):
        if not self.get_availability():
            for payload in self.current_capacity:
                if self.log[payload]["elapsed"] < self.process_time:
                    self.log[payload]["elapsed"] = self.log[payload]["elapsed"] + 1
                elif self.log[payload]["elapsed"] == self.process_time:
                    if not self.robot_needed:
                        data.payloads[payload].ready_to_pick_up()
                    self.ready_to_pick = True
                else:
                    print("ERROR")

    def get_availability(self):
        

    def release_robot(self):
        return not self.robot_needed

    def receive_payload(self, payload_id: int, time, robot_id: int):
        self.ready_to_pick = False

        self.current_capacity.append(payload_id)
        self.log[payload_id] = {"payload": payload_id,
                                "in_time": time,
                                "elapsed": 0}
        if self.robot_needed:
            data.payloads[payload_id].drop_off(robot_id)
        else:
            data.payloads[payload_id].drop_off()

    def send_out_payload(self, payload_id: int):
        self.ready_to_pick = False
        self.current_capacity.remove(payload_id)
        data.payloads[payload_id].pick_up()"""
