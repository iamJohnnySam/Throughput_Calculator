import json

from station import Station

stations = {}


with open("stations.json", "r") as file:
    station_file = json.load(file)

sequence = list(station_file.keys())

for station in station_file:
    for qty in range(station_file[station]["Stations"]):
        if station_file[station]['Attached'] != "":
            att = f"{station_file[station]['Attached']}_{str(qty)}"
        else:
            att = ""
        stations[f"{station}_{qty}"]: Station = Station(station_id=station,
                                                        time=station_file[station]["Time"],
                                                        capacity=station_file[station]["Capacity"],
                                                        robot=station_file[station]["Robot"],
                                                        buffer=station_file[station]["Buffer"],
                                                        attached_station=att)
