import json

import logging
from payload import Payload
from robot import Robot
from station import Station

with open("stations.json", "r") as file:
    station_file = json.load(file)

with open("sequence.json", "r") as file:
    sequence_file = json.load(file)
sequence = sequence_file["Sequence"]

robot1 = Robot()
stations = {}

for station in station_file:
    process_input = True if "In" in station_file[station].keys() and station_file[station]["In"] else False
    process_output = True if "Out" in station_file[station].keys() and station_file[station]["Out"] else False

    stations[station] = Station(time=station_file[station]["Time"],
                                capacity=station_file[station]["Capacity"],
                                robot=station_file[station]["Robot"],
                                process_input=process_input,
                                process_output=process_output,
                                waiting=station_file[station]["Waiting"])

payloads = {}


def create_payload(time, payload_id):
    payloads[payload_id] = Payload(time, payload_id)
    logging.log("Payload Created with ID > " + str(payload_id))
