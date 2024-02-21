import itertools
import json
import os.path
import tkinter as tk

import logging
from payload import Payload
from robot import Robot
from station import Station


class Simulation:
    smallest_time = 60

    def __init__(self, layout_name: str, sequence_frame: tk.Frame, layout_frame: tk.Frame, robot_frame: tk.Frame,
                 buffer_optimize=False):
        logging.prepare_log_file(layout_name)

        # Sequence
        self.sequence = []
        self.layout_name = layout_name

        self.buffer_optimize = buffer_optimize

        self.animate = tk.IntVar()

        # Hardware Objects
        with open(os.path.join("layouts", layout_name), "r") as file:
            station_file = json.load(file)
        self.stations = {}
        self.robots = {}
        self.transfers = {}
        self.create_hardware(station_file)
        self.last_created_process = "Null"

        # Payload objects
        self.new_payload_id = 0
        self.payloads = {}
        self.completed_payloads = 0

        # Simulation Variables
        self.sequence_frame = sequence_frame
        self.layout_frame = layout_frame
        self.robot_frame = robot_frame
        self.elapsed_time = 0
        self.setup_simulation()
        self._last_all_waiting = False
        self.deadlocked = False

    def setup_simulation(self):
        x = 0
        y = 0
        max_widgets = 8
        for st in self.stations.keys():
            if y > max_widgets:
                x = x + 1
                y = 0
            station = tk.Frame(self.layout_frame, highlightthickness=1, highlightbackground="black")
            station.grid(row=x, column=y, padx=1, pady=2, sticky='n')
            y = y + 1
            tk.Label(station, text=st, width=18, font='Helvetica 9 bold').pack()
            self.stations[st].gui = station

        for ts in self.transfers.keys():
            if y > max_widgets:
                x = x + 1
                y = 0
            station = tk.Frame(self.layout_frame, highlightthickness=1, highlightbackground="black")
            station.grid(row=x, column=y, padx=1, pady=2, sticky='n')
            y = y + 1
            tk.Label(station, text=ts, width=18, font='Helvetica 9 bold').pack()
            self.transfers[ts].gui = station

        for rbt in self.robots.keys():
            robot_item = tk.Frame(self.robot_frame, highlightthickness=1, highlightbackground="black")
            robot_item.pack(side=tk.LEFT, anchor="n", padx=1, pady=2)
            tk.Label(robot_item, text=str(rbt), font='Helvetica 9 bold').pack()
            self.robots[rbt].gui = robot_item

        sequence = ""
        for seq in self.sequence:
            if sequence == "":
                sequence += seq
            else:
                sequence += f" > {seq}"

        tk.Label(self.sequence_frame, text=sequence).pack()

        tk.Checkbutton(self.robot_frame, text="Animate", variable=self.animate, onvalue=1, offvalue=0).pack()

    def create_hardware(self, station_file: dict):
        transfer = {}
        bottleneck_time = 0
        bottleneck_process = ""
        bottleneck_area = ""
        for hardware in station_file.keys():
            hw_count = station_file[hardware]["count"]

            if "type" in station_file[hardware].keys() and station_file[hardware]["type"] == "station":
                for qty in range(hw_count):
                    time, process, area, capacity = self.create_station(hardware, qty, station_file[hardware])
                    if time > bottleneck_time and capacity > 1:
                        bottleneck_time = time
                        bottleneck_process = process
                        bottleneck_area = area

            elif "type" in station_file[hardware].keys() and station_file[hardware]["type"] == "robot":
                for qty in range(hw_count):
                    self.create_robot(hardware, qty, station_file[hardware])
            else:
                raise KeyError("Incorrect layout file. 'type' key is missing")

        if self.buffer_optimize and bottleneck_process != "":
            print(bottleneck_time, bottleneck_process, bottleneck_area)
            self.create_station("buffer", 0,
                                {
                                    "type": "station",
                                    "process": "buffer",
                                    "area": bottleneck_area,
                                    "time": 0,
                                    "capacity": 1,
                                    "count": 1,
                                    "buffer": True,
                                    "attach": ""},
                                bottleneck_process)

        for hardware in station_file.keys():
            if "type" in station_file[hardware].keys() and station_file[hardware]["type"] == "station":
                for qty in range(station_file[hardware]["count"]):
                    self.attach_station(hardware, qty, station_file[hardware])

        self.create_transfer()


    def create_robot(self, hw_name: str, num: int, hw_data: dict):
        self.robots[f'{hw_name}_{str(num)}'] = Robot(robot_id=f"{hw_data['area']}_{str(num)}",
                                                     robot_name=hw_name,
                                                     area=hw_data['area'],
                                                     get_time=hw_data['get_time'],
                                                     put_time=hw_data['put_time'])

        if self.smallest_time > hw_data['get_time'] > 5:
            self.smallest_time = hw_data['get_time']

        if self.smallest_time > hw_data['put_time'] > 5:
            self.smallest_time = hw_data['put_time']

    def create_station(self, hw_name: str, num: int, hw_data: dict, insert_before=None):
        process = hw_data['process']

        if insert_before is not None:
            self.last_created_process = self.sequence[self.sequence.index(insert_before) -1]

        if hw_data['buffer']:
            process = f'Buffer | {self.last_created_process}'

        self.stations[f'{hw_name}_{str(num)}'] = Station(process=process,
                                                         station_raw=f'{hw_name}_{str(num)}',
                                                         station_type=hw_data['type'],
                                                         time=hw_data['time'],
                                                         capacity=hw_data['capacity'],
                                                         buffer=hw_data['buffer'],
                                                         area=hw_data['area'])
        if not hw_data['buffer']:
            self.last_created_process = process

        if self.smallest_time > hw_data['time'] > 5:
            self.smallest_time = hw_data['time']

        if process not in self.sequence and insert_before is None:
            self.sequence.append(process)
        elif process not in self.sequence and insert_before is not None:
            self.sequence.insert(self.sequence.index(insert_before), process)

        return hw_data['time'], process, hw_data['area'], hw_data['capacity']

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
        combs = list(itertools.combinations(areas, 2))

        num = 0
        for ts in range(pairs):
            self.transfers[f'TRANSFER_{str(num)}'] = Station(process=f"{combs[ts][0]} > {combs[ts][1]}",
                                                             station_raw=f'TRANSFER_{str(num)}',
                                                             station_type='transfer',
                                                             time=0,
                                                             area=combs[ts][0] + "," + combs[ts][1])
            num += 1
            self.transfers[f'TRANSFER_{str(num)}'] = Station(process=f"{combs[ts][1]} > {combs[ts][0]}",
                                                             station_raw=f'TRANSFER_{str(num)}',
                                                             station_type='transfer',
                                                             time=0,
                                                             area=combs[ts][1] + "," + combs[ts][0])
            num += 1

    def get_station(self, process, check_availability=False, optimize_area=False, area=""):
        if optimize_area and area == "":
            raise AttributeError("Missing area for optimization")

        if optimize_area:
            check_availability = True

        best_station = None

        for station in self.stations:
            if self.stations[station].process == process:
                if not check_availability:
                    return station
                else:
                    if self.stations[station].available:
                        if optimize_area:
                            if self.stations[station].area == area:
                                return station
                            else:
                                best_station = station if best_station is None else best_station
                        else:
                            return station
        return best_station

    def create_payload(self, time):
        first_station = self.get_station(self.sequence[0])

        if len(self.stations[first_station].stock) < 2:
            self.new_payload_id = self.new_payload_id + 1
            self.payloads[self.new_payload_id]: Payload = Payload(create=time,
                                                                  payload_id=self.new_payload_id,
                                                                  current_station=first_station)
            logging.log("Payload Created with ID > " + str(self.new_payload_id))
            self.stations[first_station].stock.append(self.payloads[self.new_payload_id])
            self.stations[first_station].update_gui_payloads()

    def is_a_station_available(self, process) -> bool:
        for st in self.stations.keys():
            if process == self.stations[st].process and self.stations[st].available:
                return True
        return False

    def get_transfer(self, next_area, current_area):
        for tr in self.transfers.keys():
            if self.transfers[tr].area.startswith(current_area) and self.transfers[tr].area.endswith(next_area):
                return tr
        raise KeyError(f"Couldn't find appropriate transfer station")

    def get_next_station(self, payload: Payload):
        last_process = self.sequence[0]
        for seq in self.sequence:
            for visit in payload.visited_stations:
                if visit in self.stations.keys() and seq == self.stations[visit].process:
                    last_process = seq

        step = self.sequence.index(last_process)
        step = step if step == len(self.sequence) else step + 1

        if self.stations[self.get_station(self.sequence[step])].buffer:
            skip_process = self.sequence[step + 1]
            if self.is_a_station_available(skip_process):
                step = step + 1

        try:
            current_area: str = self.stations[payload.current_station].area
        except KeyError:
            current_area: str = self.transfers[payload.current_station].area.split(",")[1]

        next_process = self.sequence[step]
        next_station = self.get_station(next_process,
                                        check_availability=True,
                                        optimize_area=True, area=current_area)

        if next_station is None:
            return ""

        next_area: str = self.stations[next_station].area

        if not (current_area.endswith(next_area) or next_area.startswith(current_area)):
            next_station = self.get_transfer(next_area, current_area)

        return next_station

    def delete_completed_payloads(self):
        for payload_id in list(self.payloads.keys()):
            try:
                current_process = self.stations[self.payloads[payload_id].current_station].process
            except KeyError:
                continue
            if current_process == self.sequence[-1]:
                logging.log(f"------------- PAYLOAD {payload_id} DONE AT {self.elapsed_time} -----------------")
                print(f"PAYLOAD {payload_id} DONE AT {self.elapsed_time} ({self.elapsed_time / 3600})")
                del self.payloads[payload_id]
                self.completed_payloads = self.completed_payloads + 1

    def simulate(self, run_time: int):
        for sec in range(run_time):
            self.elapsed_time = self.elapsed_time + 1
            if self.deadlocked:
                return
            logging.log(f"\nTime = {self.elapsed_time}")
            self.create_payload(self.elapsed_time)
            self.move_payloads()
            self.run_stations()
            self.delete_completed_payloads()

    def move_payloads(self):
        all_waiting = True
        for payload_id in list(self.payloads.keys()):
            payload = self.payloads[payload_id]

            # IF PAYLOAD WAITING
            if payload.waiting:
                next_station = self.get_next_station(self.payloads[payload_id])
                if next_station == "":
                    continue
                try:
                    current_station: Station = self.stations[payload.current_station]
                except KeyError:
                    current_station: Station = self.transfers[payload.current_station]
                logging.log(f"PAYLOAD {payload_id} IS WAITING AT {payload.current_station} FOR {next_station}.")

                transfer_started = False
                for st in self.stations.keys():
                    station = self.stations[st]
                    if station.available and next_station == station.raw_name and not transfer_started:
                        transfer_started = self.try_for_pick(payload, current_station, station)

                for ts in self.transfers.keys():
                    station = self.transfers[ts]
                    if station.available and next_station == station.raw_name and not transfer_started:
                        transfer_started = self.try_for_pick(payload, current_station, station, True)

            else:
                all_waiting = False

        if all_waiting:
            self.deadlocked = True if (all_waiting and self._last_all_waiting) else False
            self._last_all_waiting = True
        else:
            self._last_all_waiting = False

    def try_for_pick(self, payload, current_station: Station, next_station: Station, transfer=False):
        for rbt in self.robots:
            robot = self.robots[rbt]

            if transfer:
                area_match = True if robot.area == current_station.area else False
            else:
                area_match = True if robot.area == next_station.area else False

            if robot.available and area_match:
                robot.pick(payload=payload,
                           current_station=current_station,
                           next_station=next_station)
                return True
        return False

    def run_stations(self):
        for robot in self.robots.keys():
            self.robots[robot].run()

        for station in self.stations.keys():
            self.stations[station].run()

        for transfer in self.transfers.keys():
            self.transfers[transfer].run()

        if self.elapsed_time % self.smallest_time == 0 and self.animate.get() == 1:
            self.layout_frame.update()
            self.robot_frame.update()
