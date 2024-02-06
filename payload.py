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

        step = sequence.index(self._current_station)
        if step == len(sequence):
            step = step
        else:
            step = step + 1
        return sequence[step]

    def robot_pickup(self):
        self.waiting = False





        """
        
        
        

        self.current_step = 0
        self.completion = False
        self.waiting = True
        self.robot_hold = None

    def get_id(self):
        return self.payload_id

    def get_step(self):
        return self.current_step

    def get_waiting(self):
        return self.waiting

    def pick_up(self):
        self.waiting = False
        self.robot_hold = None
        logging.log(f"LOADER > Picked up: " + str(self.payload_id))

    def drop_off(self, robot_id: int = None):
        self.current_step = self.current_step + 1
        if robot_id is None:
            logging.log(f"LOADER > Dropped Off: " + str(self.payload_id))
        else:
            self.robot_hold = robot_id
            logging.log(f"LOADER > Robot {str(robot_id)} Holding: {str(self.payload_id)}")

    def ready_to_pick_up(self):
        self.waiting = True
        logging.log(f"LOADER > Ready for Pick up: " + str(self.payload_id))"""


