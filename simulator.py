import itertools
import json
import os.path
import tkinter as tk

import logging
from payload import Payload
from robot import Robot
from station import Station


class Simulation:
    def __init__(self, layout_name: str, layout_frame: tk.Frame, robot_frame: tk.Frame):
        logging.prepare_log_file(layout_name)

        # Sequence
        self.sequence = []

        # Hardware Objects
        with open(os.path.join("layouts", layout_name), "r") as file:
            station_file = json.load(file)
        self.stations = {}
        self.robots = {}
        self.transfers = {}
        self.create_hardware(station_file)

        # Payload objects
        self.new_payload_id = 0
        self.payloads = {}

        # Simulation Variables
        self.elapsed_time = 0
        self.setup_simulation(layout_frame, robot_frame)

    def setup_simulation(self, layout_frame, robot_frame):
        x = 0
        y = 0
        for st in self.stations.keys():
            if y > 9:
                x = x + 1
                y = 0
            station = tk.Frame(layout_frame)
            station.grid(row=x, column=y)
            y = y + 1
            tk.Label(station, text=st, width=18, font='Helvetica 9 bold').pack()
            self.stations[st].gui = station

        for ts in self.transfers.keys():
            if y > 9:
                x = x + 1
                y = 0
            station = tk.Frame(layout_frame)
            station.grid(row=x, column=y)
            y = y + 1
            tk.Label(station, text=ts, width=18, font='Helvetica 9 bold').pack()
            self.transfers[ts].gui = station

        for rbt in self.robots.keys():
            robot_item = tk.Frame(robot_frame)
            robot_item.pack(side=tk.LEFT, anchor="n")
            tk.Label(robot_item, text=str(rbt), font='Helvetica 9 bold').pack()
            self.robots[rbt].gui = robot_item

    def create_hardware(self, station_file: dict):
        transfer = {}
        for hardware in station_file.keys():
            hw_count = station_file[hardware]["count"]

            if "type" in station_file[hardware].keys() and station_file[hardware]["type"] == "station":
                for qty in range(hw_count):
                    self.create_station(hardware, qty, station_file[hardware])
            elif "type" in station_file[hardware].keys() and station_file[hardware]["type"] == "robot":
                for qty in range(hw_count):
                    self.create_robot(hardware, qty, station_file[hardware])
            else:
                raise KeyError("Incorrect layout file. 'type' key is missing")

        for hardware in station_file.keys():
            if "type" in station_file[hardware].keys() and station_file[hardware]["type"] == "station":
                for qty in range(station_file[hardware]["count"]):
                    self.attach_station(hardware, qty, station_file[hardware])

        self.create_transfer()

    def create_robot(self, hw_name: str, num: int, hw_data: dict):
        self.robots[f'{hw_name}_{str(num)}'] = Robot(robot_id=num,
                                                     robot_name=hw_name,
                                                     area=hw_data['area'],
                                                     get_time=hw_data['get_time'],
                                                     put_time=hw_data['put_time'])

    def create_station(self, hw_name: str, num: int, hw_data: dict):
        att = f"{hw_data['attach']}_{str(num)}" if hw_data['attach'] != "" else ""
        self.stations[f'{hw_name}_{str(num)}'] = Station(station_id=hw_name,
                                                         station_raw=f'{hw_name}_{str(num)}',
                                                         station_type=hw_data['type'],
                                                         time=hw_data['time'],
                                                         capacity=hw_data['capacity'],
                                                         buffer=hw_data['buffer'],
                                                         area=hw_data['area'])
        if hw_name not in self.sequence:
            self.sequence.append(hw_name)

    def attach_station(self, hw_name: str, num: int, hw_data: dict):
        if hw_data['attach'] == "":
            return
        else:
            attach = hw_data['attach']
        self.stations[f'{hw_name}_{str(num)}'].attached_station = self.stations[f'{attach}_{str(num)}']

    def create_transfer(self):
        areas = []
        for robot in self.robots:
            if self.robots[robot].area not in areas:
                areas.append(self.robots[robot].area)

        pairs = int(len(areas) * (len(areas) - 1) / 2)
        combinations = list(itertools.combinations(areas, 2))

        for ts in range(pairs):
            self.transfers[f'TRANSFER_{str(ts)}'] = Station(station_id="TRANSFER",
                                                            station_raw=f'TRANSFER_{str(ts)}',
                                                            station_type='transfer',
                                                            time=1,
                                                            area=combinations[ts][0] + "," + combinations[ts][1])

    def create_payload(self, time):
        if len(self.stations[self.sequence[0] + "_0"].stock) < 2:
            self.new_payload_id = self.new_payload_id + 1
            self.payloads[self.new_payload_id]: Payload = Payload(create=time,
                                                                  payload_id=self.new_payload_id,
                                                                  current_station=self.sequence[0] + "_0")
            logging.log("Payload Created with ID > " + str(self.new_payload_id))

            self.stations[self.sequence[0] + "_0"].stock.append(self.payloads[self.new_payload_id])

    def is_station_available(self, station) -> bool:
        for st in self.stations.keys():
            if station == self.stations[st].station_id and self.stations[st].available:
                return True
        return False

    def get_transfer(self, area1, area2):
        for tr in self.transfers.keys():
            if area1 in self.transfers[tr].area.split(",") and area2 in self.transfers[tr].area.split(","):
                return tr
        raise KeyError("Couldn't find appropriate transfer station")

    def get_next_station(self, payload: Payload):
        last_station = self.sequence[0]
        for seq in self.sequence:
            for visit in payload.visited_stations:
                if seq == visit.split('_')[0]:
                    last_station = seq

        step = self.sequence.index(last_station)
        step = step if step == len(self.sequence) else step + 1

        if self.stations[self.sequence[step] + "_0"].buffer:
            skip_station = self.sequence[step + 1]
            if self.is_station_available(skip_station):
                step = step + 1

        next_station = self.sequence[step]

        try:
            area1 = self.stations[next_station + "_0"].area
        except KeyError:
            area1 = self.transfers[next_station + "_0"].area

        try:
            area2 = self.stations[payload.current_station].area
        except KeyError:
            area2 = self.transfers[payload.current_station].area

        if not (area1 in area2.split(",") or area2 in area1.split(",")):
            next_station = self.get_transfer(area1, area2)

        return next_station

    def delete_completed_payloads(self):
        for payload_id in list(self.payloads.keys()):
            if self.payloads[payload_id].current_station.split('_')[0] == self.sequence[-1]:
                logging.log(f"------------- PAYLOAD {payload_id} DONE AT {self.elapsed_time} -----------------")
                print(f"PAYLOAD {payload_id} DONE AT {self.elapsed_time} ({self.elapsed_time / 3600})")
                del self.payloads[payload_id]

    def simulate(self, run_time: int):
        for sec in range(run_time):
            logging.log(f"\nTime = {self.elapsed_time}")
            self.create_payload(self.elapsed_time)
            self.move_payloads()
            self.run_stations()
            self.delete_completed_payloads()
            self.elapsed_time = self.elapsed_time + 1

    def move_payloads(self):
        for payload_id in list(self.payloads.keys()):
            payload = self.payloads[payload_id]
            # IF PAYLOAD WAITING
            if payload.waiting:
                next_station = self.get_next_station(self.payloads[payload_id])
                try:
                    current_station: Station = self.stations[payload.current_station]
                except KeyError:
                    current_station: Station = self.transfers[payload.current_station]
                logging.log(f"PAYLOAD {payload_id} IS WAITING AT {payload.current_station} FOR {next_station}.")

                transfer_started = False
                for st in self.stations.keys():
                    station = self.stations[st]
                    if station.available and next_station == station.station_id and not transfer_started:
                        transfer_started = self.try_for_pick(payload, current_station, station)

                for ts in self.transfers.keys():
                    station = self.transfers[ts]
                    if station.available and next_station == station.raw_name and not transfer_started:
                        transfer_started = self.try_for_pick(payload, current_station, station, True)

    def try_for_pick(self, payload, current_station, station, transfer=False):
        for rbt in self.robots:
            robot = self.robots[rbt]

            if transfer:
                area_match = True if robot.area == current_station.area else False
                print(robot.area)
                print(current_station.area)
            else:
                area_match = True if robot.area == station.area else False

            if robot.available and area_match:
                robot.pick(payload=payload,
                           current_station=current_station,
                           next_station=station)
                return True
        return False

    def run_stations(self):
        for robot in self.robots.keys():
            self.robots[robot].run()

        for station in self.stations.keys():
            self.stations[station].run()

        for transfer in self.transfers.keys():
            self.transfers[transfer].run()
