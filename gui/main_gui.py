import json
import os

import tkinter as tk
from datetime import datetime

from gui.layout_manager import LayoutManager
from gui.new_layout import LayoutEditor
from simulator import Simulation


class GUI:
    def __init__(self, root):
        self.animate = tk.BooleanVar()
        self.log_process = tk.BooleanVar()

        title = "ROBOT LAYOUT SIMULATOR"

        self.master = root
        self.master.title(title)

        menubar = tk.Menu(self.master, tearoff=0)

        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Simulation', menu=file)
        file.add_command(label='New Layout', command=self.create_layout)
        file.add_command(label='Manage Layouts', command=self.manage_layouts)
        file.add_command(label='Exit', command=self.master.destroy)

        execute = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Execute', menu=execute)
        execute.add_checkbutton(label='Animate', onvalue=1, offvalue=0, variable=self.animate)
        execute.add_separator()
        execute.add_checkbutton(label='Log Process', onvalue=1, offvalue=0, variable=self.log_process)
        execute.add_separator()
        execute.add_command(label='Run all', command=self.run_all_layouts)
        execute.add_command(label='Run all with buffer optimization', command=self.buffer_optimize_all)
        execute.add_command(label='Run all and buffer optimize', command=self.run_buffer_optimize_all)
        self.master.config(menu=menubar)

        tk.Label(self.master, text=title, font=("Calibri", 20)).pack()

        # LAYOUT SELECTION FRAME
        layout_frame = tk.Frame(self.master)
        layout_options = os.listdir("layouts")

        longest_text = 25
        for lay in layout_options:
            text_len = len(lay)
            if text_len > longest_text:
                longest_text = text_len

        self.selected_layout = tk.StringVar()
        self.layout_drop = tk.OptionMenu(layout_frame, self.selected_layout, *layout_options)
        self.layout_drop.config(width=75)
        self.layout_drop.pack(side=tk.LEFT, padx=5)
        self.layout_button = tk.Button(layout_frame, text="Select Layout", command=self.layout_selected)
        self.layout_button.pack(side=tk.LEFT, padx=5)
        self.layout_buffer = tk.Button(layout_frame, text="Buffer Optimize", command=self.buffer_optimize)
        self.layout_buffer.pack(side=tk.LEFT, padx=5)
        self.layout_optimize = tk.Button(layout_frame, text="Layout Optimize", command=self.layout_optimize)
        self.layout_optimize.pack(side=tk.LEFT, padx=5)

        tk.Label(self.master).pack()

        layout_frame.pack()
        tk.Label(self.master).pack()

        # SIMULATION CONTROLS LAYOUT
        self.controls_frame = tk.Frame(self.master)
        self.controls_frame.pack()
        self._gui_elapsed_time = tk.Label(self.controls_frame, text="SELECT A LAYOUT")
        self._gui_elapsed_time.pack()

        btn_gap = 2
        self.btn_01sc = tk.Button(self.controls_frame, text="Simulate 1 sec", command=self.simulate_1s,
                                  state=tk.DISABLED)
        self.btn_01sc.pack(side=tk.LEFT, padx=btn_gap)
        self.btn_15sc = tk.Button(self.controls_frame, text="Simulate 15sec", command=self.simulate_15s,
                                  state=tk.DISABLED)
        self.btn_15sc.pack(side=tk.LEFT, padx=btn_gap)
        self.btn_30sc = tk.Button(self.controls_frame, text="Simulate 30sec", command=self.simulate_30s,
                                  state=tk.DISABLED)
        self.btn_30sc.pack(side=tk.LEFT, padx=btn_gap)
        self.btn_30mn = tk.Button(self.controls_frame, text="Simulate 30min", command=self.simulate_30m,
                                  state=tk.DISABLED)
        self.btn_30mn.pack(side=tk.LEFT, padx=btn_gap)
        self.btn_01hr = tk.Button(self.controls_frame, text="Simulate 1hour", command=self.simulate_1h,
                                  state=tk.DISABLED)
        self.btn_01hr.pack(side=tk.LEFT, padx=btn_gap)

        tk.Label(self.controls_frame, width=btn_gap).pack(side=tk.LEFT)
        v_cmd = self.controls_frame.register(self.validate_input)
        self.run_time_entry = tk.Entry(self.controls_frame, width=5, validate="key",
                                       validatecommand=(v_cmd, '%d', '%P'))
        self.run_time_entry.pack(side=tk.LEFT)
        self.btn_x_sc = tk.Button(self.controls_frame, text="Simulate 10s", command=self.simulate_x, state=tk.DISABLED)
        self.btn_x_sc.pack(side=tk.LEFT, padx=btn_gap)
        self.run_time_entry.insert(0, "10")
        self.btn_22fn = tk.Button(self.controls_frame, text="Complete 22h", command=self.simulate_remaining,
                                  state=tk.DISABLED)
        self.btn_22fn.pack(side=tk.LEFT, padx=btn_gap)
        tk.Label(self.master).pack()

        # SEQUENCE FRAME
        self.sequence_frame = tk.Frame(self.master)
        self.sequence_frame.pack()
        tk.Label().pack()

        # LAYOUT FRAME
        self.layout_frame = tk.Frame(self.master)
        self.layout_frame.pack()

        # ROBOT FRAME
        self.robot_frame = tk.Frame(self.master)
        self.robot_frame.pack()

        for layout_name in os.listdir("layouts"):
            path = os.path.join("layouts", layout_name)
            with open(path, "r") as file:
                station_file = json.load(file)
            if station_file == {}:
                os.remove(path)

        self.sim: Simulation = Simulation(os.listdir("layouts")[0],
                                          self.sequence_frame, self.layout_frame, self.robot_frame,
                                          log=self.log_process.get())

    def run_all_layouts(self):
        for layout in list(os.listdir("layouts")):
            self.layout_selected(layout)
            self.simulate_remaining()

    def buffer_optimize_all(self):
        for layout in list(os.listdir("layouts")):
            self.layout_selected(layout, buffer_optimize=True)
            self.simulate_remaining()

    def run_buffer_optimize_all(self):
        for layout in list(os.listdir("layouts")):
            self.layout_selected(layout)
            self.simulate_remaining()
            self.layout_selected(layout, buffer_optimize=True)
            self.simulate_remaining()

    def buffer_optimize(self):
        self.layout_selected(self.selected_layout.get(), buffer_optimize=True)

    def layout_optimize(self):
        self.layout_selected(self.selected_layout.get(), layout_optimize=True)

    def layout_selected(self, layout="", buffer_optimize=False, layout_optimize=False):
        if layout == "":
            layout = self.selected_layout.get()

        if layout == "":
            return

        for widget in self.sequence_frame.winfo_children():
            widget.destroy()

        for widget in self.layout_frame.winfo_children():
            widget.destroy()

        for widget in self.robot_frame.winfo_children():
            widget.destroy()

        self.btn_01sc["state"] = tk.ACTIVE
        self.btn_15sc["state"] = tk.ACTIVE
        self.btn_30sc["state"] = tk.ACTIVE
        self.btn_30mn["state"] = tk.ACTIVE
        self.btn_01hr["state"] = tk.ACTIVE
        self.btn_x_sc["state"] = tk.ACTIVE
        self.btn_22fn["state"] = tk.ACTIVE

        lbl_selected_layout = tk.Label(self.sequence_frame, text="Layout : " + str(layout))
        lbl_selected_layout.pack()
        lbl_selected_layout.update()

        self.sim = Simulation(layout, self.sequence_frame, self.layout_frame, self.robot_frame,
                              buffer_optimize=buffer_optimize,
                              layout_optimize=layout_optimize,
                              log=self.log_process.get())
        self.updated_sim_time()

    def validate_input(self, action, value_if_allowed):
        if action == '1':  # insert
            if value_if_allowed.isdigit():
                self.btn_x_sc["text"] = f"Simulate {value_if_allowed}s"
                return True
            else:
                return False
        else:
            return True

    def updated_sim_time(self):
        if self.sim.deadlocked:
            self._gui_elapsed_time["text"] = f"STATIONS REACHED DEADLOCK CONDITION AT {str(self.sim.elapsed_time)} SEC"
            self._gui_elapsed_time["fg"] = 'black'
            self._gui_elapsed_time["bg"] = 'red'
        else:
            self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.sim.elapsed_time)}sec\t"
                                              f"{str(self.sim.elapsed_time / 3600)}hours")

    def simulate(self, time):
        self.layout_drop["state"] = "disabled"
        self.layout_button["state"] = "disabled"
        self.layout_buffer["state"] = "disabled"
        self.layout_optimize["state"] = "disabled"

        time_jump = 30
        time_intervals = int(time / time_jump)
        time_left = time % time_jump

        for jump in range(time_intervals):
            self.sim.simulate(time_jump)
            self.updated_sim_time()
            if self.animate.get():
                self.robot_frame.update()
                self.layout_frame.update()
                self._gui_elapsed_time.update()
        self.sim.simulate(time_left)
        self.updated_sim_time()

        if self.sim.elapsed_time >= (22 * 60 * 60) > self.sim.elapsed_time - time:
            self.record()

        self.layout_drop["state"] = tk.NORMAL
        self.layout_button["state"] = tk.NORMAL
        self.layout_buffer["state"] = tk.NORMAL
        self.layout_optimize["state"] = tk.NORMAL

    def simulate_1s(self):
        self.simulate(1)

    def simulate_15s(self):
        self.simulate(15)

    def simulate_30s(self):
        self.simulate(30)

    def simulate_30m(self):
        self.simulate(30 * 60)

    def simulate_1h(self):
        self.simulate(60 * 60)

    def simulate_x(self):
        self.simulate(int(self.run_time_entry.get()))

    def simulate_remaining(self):
        self.simulate((22 * 60 * 60) - self.sim.elapsed_time)

    def record(self):
        path = "log/log.txt"
        if not os.path.isfile(path):
            file = open(path, "w")

        station_details = ""
        robot_details = ""
        transfer_details = ""

        for rbt in self.sim.robots:
            robot = self.sim.robots[rbt]
            val = (f"{robot.robot_name}\t"
                   f"{robot.robot_id}\t"
                   f"{robot.area}\t"
                   f"{robot.get_time}\t"
                   f"{robot.put_time}")
            robot_details = robot_details + val + "\n"

        for stat in self.sim.stations:
            station = self.sim.stations[stat]
            val = (f"{station.process}\t"
                   f"{station.raw_name}\t"
                   f"{station.type}\t"
                   f"{station.run_time}\t"
                   f"{station.max_capacity}\t"
                   f"{station.buffer}\t"
                   f"{station.area}")
            station_details = station_details + val + "\n"

        for tra in self.sim.transfers:
            station = self.sim.transfers[tra]
            val = (f"{station.process}\t"
                   f"{station.raw_name}\t"
                   f"{station.type}\t"
                   f"{station.run_time}\t"
                   f"{station.max_capacity}\t"
                   f"{station.buffer}\t"
                   f"{station.area}")
            transfer_details = transfer_details + val + "\n"

        f = open(path, "a")
        f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:S")}\n'
                f'Layout Name: {self.sim.layout_name}\n'
                f'ROBOTS\n'
                f'Name\tID\tArea\tGet Time\tPut Time\n'
                f'{robot_details}'
                f'STATIONS\n'
                f'Process\tName\tType\tTime\tCapacity\tIs Buffer\tArea\n'
                f'{station_details}'
                f'{transfer_details}'
                f'Output: {str(self.sim.completed_payloads)} in {self.sim.elapsed_time} seconds '
                f'({self.sim.elapsed_time/3600} hours).\n\n')
        f.close()

    def create_layout(self, layout=""):
        LayoutEditor(self.master, layout=layout)

    def manage_layouts(self):
        LayoutManager(self.master)
