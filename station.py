import json

import data
import logging
from payload import Payload


class Station:
    def __init__(self, station_id, time, capacity: int = 1, robot: bool = False, process_input: bool = False,
                 process_output: bool = False,
                 waiting: bool = True):

        self._station_id = station_id
        self._process_time = 0
        self._stock = list()
        self._capacity = capacity
        self._robot_needed = robot
        self._robot_release = not robot
        self._time = time

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
            self._process_time = self._process_time + 1
            if self._time > self._process_time:
                pass
            elif self._time == self._process_time:
                self._robot_release = True
                if not self._robot_needed:
                    for item in self._stock:
                        item.waiting = True

