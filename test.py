import tkinter as tk
import time


class Payload:
    def __init__(self, number, cycle_time):
        self.number = number
        self.cycle_time = cycle_time
        self.current_location = None
        self.remaining_cycle_time = cycle_time


class Station:
    def __init__(self, x, y, number_of_payloads, cycle_time):
        self.x = x
        self.y = y
        self.number_of_payloads = number_of_payloads
        self.cycle_time = cycle_time
        self.payloads = [Payload(i + 1, cycle_time) for i in range(number_of_payloads)]


class Robot:
    def __init__(self, x, y, transfer_time):
        self.x = x
        self.y = y
        self.transfer_time = transfer_time
        self.payload = None


class Simulator:
    def __init__(self, master, grid_size=10):
        self.master = master
        self.grid_size = grid_size
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.stations = []
        self.robot = None
        self.canvas.bind("<Button-1>", self.create_station)
        self.setup_simulation()

    def setup_simulation(self):
        self.create_station(0)  # Create loading station
        self.create_station(9)  # Create unloading station
        self.create_robot()

    def create_station(self, event):
        if isinstance(event, int):
            x, y = self.canvas.canvasx(self.canvas.winfo_pointerx()), self.canvas.canvasy(self.canvas.winfo_pointery())
        else:
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

        station_window = tk.Toplevel(self.master)
        tk.Label(station_window, text="Number of Payloads:").grid(row=0, column=0)
        tk.Label(station_window, text="Cycle Time:").grid(row=1, column=0)
        number_of_payloads_entry = tk.Entry(station_window)
        cycle_time_entry = tk.Entry(station_window)
        number_of_payloads_entry.grid(row=0, column=1)
        cycle_time_entry.grid(row=1, column=1)

        def add_station():
            number_of_payloads = int(number_of_payloads_entry.get())
            cycle_time = int(cycle_time_entry.get())
            self.stations.append(Station(x, y, number_of_payloads, cycle_time))
            self.draw_station(x, y)
            station_window.destroy()

        tk.Button(station_window, text="Add Station", command=add_station).grid(row=2, columnspan=2)

    def create_robot(self):
        self.robot = Robot(4, 4, 1)
        self.draw_robot()

    def draw_station(self, x, y):
        self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill="blue")

    def draw_robot(self):
        self.canvas.create_rectangle(self.robot.x - 10, self.robot.y - 10,
                                     self.robot.x + 10, self.robot.y + 10, fill="red")

    def move_payload(self, payload, source, destination):
        self.master.update()
        time.sleep(self.robot.transfer_time)
        payload.current_location = destination

    def simulate(self):
        for station in self.stations:
            for payload in station.payloads:
                payload.current_location = station

        for station in self.stations:
            for payload in station.payloads:
                self.move_payload(payload, station, self.stations[-1])


root = tk.Tk()
simulator = Simulator(root)
tk.Button(root, text="Start Simulation", command=simulator.simulate).pack()
root.mainloop()
