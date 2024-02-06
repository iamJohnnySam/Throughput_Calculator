import data
import logging
from payload import Payload


class Robot:
    def __init__(self, robot_id):
        self._robot_id = robot_id

        self._stock = []
        self._capacity = 1

        self._current_time = 0
        self._get_action = False
        self._put_action = False
        self._at_station = False

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

    def pick(self, payload: Payload):
        payload.robot_pickup()
        self._stock.append(payload)
        self._current_time = 0
        self._get_action = True
        self._put_action = False
        self._at_station = False

    def place(self, payload: Payload, next_station: str):
        logging.log(f"ROBOT {self._robot_id} PLACE INITIATED FOR PAYLOAD {payload.payload_id} TO {next_station}")
        payload.robot_pickup()
        self._current_time = 0
        self._get_action = False
        self._put_action = True
        self._at_station = False
        payload.current_station = next_station

    def run(self):
        if self._get_action:
            self._current_time = self._current_time + 1

            if self._current_time < self._transfer_time and data.stations[self.stock[0].current_station].robot_release:
                self.place(self.stock[0], self.stock[0].next_station)
                self._get_action = False

            elif self._current_time == self._transfer_time:
                logging.log(f"ROBOT {self._robot_id} > PAYLOAD {self.stock[0].payload_id} AT {self.stock[0].current_station}")
                self._at_station = True

                data.stations[self.stock[0].current_station].robot_pickup(self.stock[0])

        if self._put_action:
            if self._current_time < self._transfer_time:
                self._current_time = self._current_time + 1
            else:
                logging.log(f"ROBOT {self._robot_id} > PLACE ARRIVE {self.stock[0].payload_id} AT {self.stock[0].current_station}")
                self._put_action = False
                self._at_station = True
                self._stock.remove(self.stock[0])

                data.stations[self.stock[0].current_station].robot_place(self.stock[0])

        """
        

        self.current_capacity = []
        self.log = {}

        self.get_time = 15
        self.put_time = 15

        self.transfer_id = 0

    def run(self, time):
        if len(self.current_capacity) == self.capacity:
            for transfer in self.current_capacity:

                if self.log[transfer]["get_elapsed"] < self.get_time:
                    self.log[transfer]["get_elapsed"] = self.log[transfer]["get_elapsed"] + 1

                elif self.log[transfer]["get_elapsed"] >= self.get_time:
                    if self.log[transfer]["robot_released"]:
                        if self.log[transfer]["put_elapsed"] < self.put_time:
                            self.log[transfer]["put_elapsed"] = self.log[transfer]["put_elapsed"] + 1

                        elif self.log[transfer]["put_elapsed"] == self.put_time:
                            self.log[transfer]["get_elapsed"] = self.log[transfer]["get_elapsed"] + 1
                            self.place(transfer, release=True, time=time)

                    else:
                        if self.log[transfer]["get_elapsed"] == self.get_time:
                            self.place(transfer, release=False, time=time)

                        self.log[transfer]["get_elapsed"] = self.log[transfer]["get_elapsed"] + 1

                        if data.stations[self.log[transfer]["next_station"]].ready_to_pick:
                            self.pick(time, self.log[transfer]["payload_id"], )
                            self.log[transfer]["robot_released"] = True
                            data.stations[self.log[transfer]["next_station"]].send_out_payload(self.log[transfer]["payload"])


    def place(self, transfer_id, release: bool, time):
        data.payloads[self.log[transfer_id]["payload_id"]].drop_off()
        data.stations[self.log[transfer_id]["next_station"]].receive_payload(self.log[transfer_id]["payload_id"], time)

        if release:
            self.current_capacity.remove(transfer_id)
            logging.log(f'ROBOT > PLACE {self.log[transfer_id]["payload_id"]} '
                        f'> TO {self.log[transfer_id]["next_station"]}')"""
