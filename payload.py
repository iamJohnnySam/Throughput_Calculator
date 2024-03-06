import logging


class Payload:
    def __init__(self, create: int, payload_id: int, current_station: str, log=False):
        self.create_time = create
        self.payload_id = payload_id

        self._waiting = True

        self._current_station = current_station
        self.visited_stations = []

        self.log = log

    @property
    def waiting(self):
        return self._waiting

    @waiting.setter
    def waiting(self, val: bool):
        self._waiting = val
        if self.log:
            logging.log(f"PAYLOAD {self.payload_id} WAITING = {val}")

    @property
    def current_station(self):
        return self._current_station

    @current_station.setter
    def current_station(self, station: str):
        self._current_station = station
        self.visited_stations.append(station)

    def robot_pickup(self):
        self.waiting = False
