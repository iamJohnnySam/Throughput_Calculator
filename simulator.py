import tkinter as tk

import data
import logging
from payload import Payload
from robot import Robot

new_payload_id = 0
input_every = 1000
robots = {1: Robot(1)}
# robots = {1: Robot(1),
#           2: Robot(2)}
payloads = {}


def create_payload(time):
    global new_payload_id

    if len(data.stations[data.sequence[0] + "_0"].stock) < 2:
        new_payload_id = new_payload_id + 1
        payloads[new_payload_id]: Payload = Payload(create=time,
                                                    payload_id=new_payload_id,
                                                    current_station=data.sequence[0] + "_0")
        logging.log("Payload Created with ID > " + str(new_payload_id))

        data.stations[data.sequence[0] + "_0"].stock.append(payloads[new_payload_id])


class Simulator:
    def __init__(self, master, grid_size=10):
        self.master = master
        self.grid_size = grid_size
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()

        self.process_time = 22 * 60 * 60
        self.elapsed_time = 0

        # Frames
        self.stations_frame = tk.Frame(self.canvas)
        self.stations_frame.pack()
        self._gui_elapsed_time = tk.Label(self.canvas, text="SIMULATION NOT STARTED")

        self.setup_simulation()

    def setup_simulation(self):
        for st in data.stations.keys():
            station = tk.Frame(self.stations_frame)
            station.pack(side=tk.LEFT)
            tk.Label(station, text=st, width=18).pack()
            data.stations[st].gui = station
        tk.Label(self.canvas).pack()

        robot_frame = tk.Frame(self.canvas)
        robot_frame.pack()
        for rbt in robots.keys():
            robot_item = tk.Frame(robot_frame)
            robot_item.pack()
            tk.Label(robot_item, text="ROBOT " + str(rbt)).pack()
            robots[rbt].gui = robot_item

        buttons_frame = tk.Frame(self.canvas)
        buttons_frame.pack()
        tk.Label(self.canvas).pack()

        self._gui_elapsed_time.pack()
        tk.Button(buttons_frame, text="Simulate 15sec", command=self.simulate_15s).pack(side=tk.LEFT)
        tk.Button(buttons_frame, text="Simulate 30sec", command=self.simulate_30s).pack(side=tk.LEFT)
        tk.Button(buttons_frame, text="Simulate 1hour", command=self.simulate_1h).pack(side=tk.LEFT)
        tk.Button(buttons_frame, text="Complete Simulation", command=self.simulate_remaining).pack(side=tk.LEFT)

    def simulate_15s(self):
        self.simulate(15)

    def simulate_30s(self):
        self.simulate(15)

    def simulate_1h(self):
        self.simulate(60 * 60)

    def simulate_remaining(self):
        self.simulate(self.process_time - self.elapsed_time)

    def simulate(self, run_time: int):
        for sec in range(run_time):
            logging.log(f"\nTime = {self.elapsed_time}")

            create_payload(self.elapsed_time)

            for payload_id in list(payloads.keys()):
                if payloads[payload_id].current_station.split('_')[0] == data.sequence[-1]:
                    logging.log(f"------------- PAYLOAD {payload_id} DONE AT {self.elapsed_time} -----------------")
                    print(f"------------- PAYLOAD {payload_id} DONE AT {self.elapsed_time} -----------------")
                    del payloads[payload_id]
                    continue

                # IF PAYLOAD WAITING
                if payloads[payload_id].waiting:
                    logging.log(f"PAYLOAD {payload_id} IS WAITING AT {payloads[payload_id].current_station}")
                    next_station = payloads[payload_id].next_station

                    transfer_started = False
                    for st in data.stations.keys():
                        if data.stations[st].available and next_station == data.stations[st].station_id and not transfer_started:

                            for robot in robots:
                                if robots[robot].available and not transfer_started:
                                    logging.log(f"ROBOT {robots[robot].robot_id} > Pick up Initiated for "
                                                f"Payload {str(payload_id)} transfer to {st}.")
                                    robots[robot].pick(payload=payloads[payload_id], next_station=st)
                                    transfer_started = True

                        else:
                            pass
                            # logging.log(f"PAYLOAD {payload_id} CANNOT TRANSFER TO {st}")

            for robot in robots.keys():
                robots[robot].run()

            for station in data.stations.keys():
                data.stations[station].run()

            self.elapsed_time = self.elapsed_time + 1
            self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.elapsed_time)}sec\t"
                                              f"{str(self.elapsed_time / 3600)}hours")
