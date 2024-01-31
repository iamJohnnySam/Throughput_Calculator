import data
from payload import Payload


class Station:
    def __init__(self, time, capacity=1, robot: bool = False, process_input: bool = False, process_output: bool = False,
                 waiting: bool = True):
        self.process_time = time
        self.log = {}
        self.capacity = capacity
        self.robot_needed = robot
        self.current_capacity = []
        self.ready_to_pick = False

    def run(self, time):
        if self.get_availability() == 0:
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
        return len(self.current_capacity) < self.capacity

    def release_robot(self):
        return not self.robot_needed

    def receive_payload(self, payload_id: int, time):
        self.ready_to_pick = False
        self.current_capacity.append(payload_id)
        self.log[payload_id] = {"payload": payload_id,
                                "in_time": time,
                                "elapsed": 0}

    def send_out_payload(self, payload_id: int):
        self.ready_to_pick = False
        self.current_capacity.remove(payload_id)
