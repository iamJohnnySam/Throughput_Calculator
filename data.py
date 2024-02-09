import json

from station import Station

stations = {}


with open("stations.json", "r") as file:
    station_file = json.load(file)

sequence = list(station_file.keys())

for station in station_file:
    process_input = True if "In" in station_file[station].keys() and station_file[station]["In"] else False
    process_output = True if "Out" in station_file[station].keys() and station_file[station]["Out"] else False

    for qty in range(station_file[station]["Stations"]):
        stations[f"{station}_{qty}"]: Station = Station(station_id=station,
                                                        time=station_file[station]["Time"],
                                                        capacity=station_file[station]["Capacity"],
                                                        robot=station_file[station]["Robot"],
                                                        process_input=process_input,
                                                        process_output=process_output,
                                                        waiting=station_file[station]["Waiting"],
                                                        buffer=station_file[station]["Buffer"])
