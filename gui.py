import os
import tkinter as tk

from simulator import Simulation


class Simulator:
    def __init__(self, master):
        title = "ROBOT LAYOUT SIMULATOR"

        master.title(title)
        tk.Label(master, text=title, font=("Calibri", 20)).pack()

        # LAYOUT SELECTION FRAME
        layout_frame = tk.Frame(master)
        layout_options = os.listdir("layouts")

        longest_text = 25
        for lay in layout_options:
            text_len = len(lay)
            if text_len > longest_text:
                longest_text = text_len

        self.selected_layout = tk.StringVar()
        self.layout_drop = tk.OptionMenu(layout_frame, self.selected_layout, *layout_options)
        self.layout_drop.config(width=75)
        self.layout_drop.pack(side=tk.LEFT)
        self.layout_button = tk.Button(layout_frame, text="Select Layout", command=self.layout_selected)
        self.layout_button.pack(side=tk.LEFT)
        tk.Label(master).pack()
        layout_frame.pack()
        tk.Label(master).pack()

        # SIMULATION CONTROLS LAYOUT
        controls_frame = tk.Frame(master)
        controls_frame.pack()
        self._gui_elapsed_time = tk.Label(controls_frame, text="SELECT A LAYOUT")
        self._gui_elapsed_time.pack()

        self.btn_01sc = tk.Button(controls_frame, text="Simulate 1 sec", command=self.simulate_1s, state=tk.DISABLED)
        self.btn_01sc.pack(side=tk.LEFT)
        self.btn_15sc = tk.Button(controls_frame, text="Simulate 15sec", command=self.simulate_15s, state=tk.DISABLED)
        self.btn_15sc.pack(side=tk.LEFT)
        self.btn_30sc = tk.Button(controls_frame, text="Simulate 30sec", command=self.simulate_30s, state=tk.DISABLED)
        self.btn_30sc.pack(side=tk.LEFT)
        self.btn_30mn = tk.Button(controls_frame, text="Simulate 30min", command=self.simulate_30m, state=tk.DISABLED)
        self.btn_30mn.pack(side=tk.LEFT)
        self.btn_01hr = tk.Button(controls_frame, text="Simulate 1hour", command=self.simulate_1h, state=tk.DISABLED)
        self.btn_01hr.pack(side=tk.LEFT)

        tk.Label(controls_frame, width=5).pack(side=tk.LEFT)
        v_cmd = controls_frame.register(self.validate_input)
        self.run_time_entry = tk.Entry(controls_frame, width=5, validate="key", validatecommand=(v_cmd, '%d', '%P'))
        self.run_time_entry.pack(side=tk.LEFT)
        self.btn_x_sc = tk.Button(controls_frame, text="Simulate 10s", command=self.simulate_x, state=tk.DISABLED)
        self.btn_x_sc.pack(side=tk.LEFT)
        self.run_time_entry.insert(0, "10")
        self.btn_22fn = tk.Button(controls_frame, text="Complete 22h", command=self.simulate_remaining,
                                  state=tk.DISABLED)
        self.btn_22fn.pack()
        tk.Label(master).pack()

        # LAYOUT FRAME
        self.layout_frame = tk.Frame(master)
        self.layout_frame.pack()

        # ROBOT FRAME
        self.robot_frame = tk.Frame(master)
        self.robot_frame.pack()

        self.sim = None

    def layout_selected(self):
        if self.selected_layout.get() == "":
            return

        self.layout_drop["state"] = "disabled"
        self.layout_button["state"] = "disabled"
        self.btn_01sc["state"] = tk.ACTIVE
        self.btn_15sc["state"] = tk.ACTIVE
        self.btn_30sc["state"] = tk.ACTIVE
        self.btn_30mn["state"] = tk.ACTIVE
        self.btn_01hr["state"] = tk.ACTIVE
        self.btn_x_sc["state"] = tk.ACTIVE
        self.btn_22fn["state"] = tk.ACTIVE

        self.sim = Simulation(self.selected_layout.get(), self.layout_frame, self.robot_frame)


    def validate_input(self, action, value_if_allowed):
        if action == '1':  # insert
            if value_if_allowed.isdigit():
                self.btn_x_sc["text"] = f"Simulate {value_if_allowed}s"
                return True
            else:
                return False
        else:
            return True

    def simulate_1s(self):
        self.sim.simulate(1)
        self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.sim.elapsed_time)}sec\t"
                                          f"{str(self.sim.elapsed_time / 3600)}hours")

    def simulate_15s(self):
        self.sim.simulate(15)
        self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.sim.elapsed_time)}sec\t"
                                          f"{str(self.sim.elapsed_time / 3600)}hours")

    def simulate_30s(self):
        self.sim.simulate(30)
        self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.sim.elapsed_time)}sec\t"
                                          f"{str(self.sim.elapsed_time / 3600)}hours")

    def simulate_30m(self):
        self.sim.simulate(30 * 60)
        self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.sim.elapsed_time)}sec\t"
                                          f"{str(self.sim.elapsed_time / 3600)}hours")

    def simulate_1h(self):
        self.sim.simulate(60 * 60)
        self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.sim.elapsed_time)}sec\t"
                                          f"{str(self.sim.elapsed_time / 3600)}hours")

    def simulate_x(self):
        self.sim.simulate(int(self.run_time_entry.get()))
        self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.sim.elapsed_time)}sec\t"
                                          f"{str(self.sim.elapsed_time / 3600)}hours")

    def simulate_remaining(self):
        self.sim.simulate((22 * 60 * 60) - self.sim.elapsed_time)
        self._gui_elapsed_time["text"] = (f"SIMULATION TIME = {str(self.sim.elapsed_time)}sec\t"
                                          f"{str(self.sim.elapsed_time / 3600)}hours")
