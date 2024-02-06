import json

import logging


class Payload:
    def __init__(self, create: int, payload_id: int, current_station: str):
        self._create_time = create
        self._payload_id = payload_id

        self._waiting = True

        self._current_station = current_station

    @property
    def payload_id(self):
        return self._payload_id

    @property
    def waiting(self):
        return self._waiting

    @waiting.setter
    def waiting(self, val: bool):
        self._waiting = val
        logging.log(f"PAYLOAD {self._payload_id} WAITING = {val}")

    @property
    def current_station(self):
        return self._current_station

    @current_station.setter
    def current_station(self, station: str):
        self._current_station = station

    @property
    def next_station(self):
        with open("sequence.json", "r") as file:
            sequence_file = json.load(file)
        sequence: list = sequence_file["Sequence"]

        step = sequence.index(self._current_station.split('_')[0])
        if step == len(sequence):
            step = step
        else:
            step = step + 1
        return sequence[step]

    def robot_pickup(self):
        self.waiting = False


