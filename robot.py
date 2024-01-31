import data
import logging


class Robot:
    def __init__(self):
        self.current_capacity = []
        self.log = {}
        self.capacity = 1

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

    def pick(self, time, payload_id: int, station: str, p_station: str):
        data.payloads[payload_id].pick_up()
        data.stations[p_station].send_out_payload(payload_id)
        self.current_capacity.append(self.transfer_id)
        self.log[self.transfer_id] = {"payload_id": payload_id,
                                      "next_station": station,
                                      "in_time": time,
                                      "robot_released": not data.stations[station].robot_needed,
                                      "get_elapsed": 0,
                                      "put_elapsed": 0}
        self.transfer_id = self.transfer_id + 1
        logging.log(f"ROBOT > PICK {payload_id} > FROM {station}")

    def place(self, transfer_id, release: bool, time):
        data.payloads[self.log[transfer_id]["payload_id"]].drop_off()
        data.stations[self.log[transfer_id]["next_station"]].receive_payload(self.log[transfer_id]["payload_id"], time)

        if release:
            self.current_capacity.remove(transfer_id)
            logging.log(f'ROBOT > PLACE {self.log[transfer_id]["payload_id"]} '
                        f'> TO {self.log[transfer_id]["next_station"]}')
