import json

import data
import logging
from payload import Payload
from robot import Robot
from station import Station

process_time = 22 * 60 * 60
input_every = 600
new_payload_id = 0
robots = {1: Robot(1)}
payloads = {}


with open("sequence.json", "r") as file:
    sequence_file = json.load(file)
sequence = sequence_file["Sequence"]

for sec in range(process_time):
    logging.log(f"\nTime = {sec}")
    print(sec)

    if sec % input_every == 0:
        new_payload_id = new_payload_id + 1
        payloads[new_payload_id]: Payload = Payload(create=sec,
                                                    payload_id=new_payload_id,
                                                    current_station=sequence[0])
        logging.log("Payload Created with ID > " + str(new_payload_id))

        data.stations[sequence[0]].stock.append(payloads[new_payload_id])

    for payload_id in payloads.keys():
        # IF PAYLOAD WAITING
        if payloads[payload_id].waiting:
            next_station = payloads[payload_id].next_station

            if data.stations[next_station].available:
                for robot in robots:
                    if robots[robot].available:
                        logging.log(f"ROBOT {robots[robot].robot_id} > Pick up Initiated for "
                                    f"Payload {str(payload_id)} at {next_station}.")
                        robots[robot].pick(payload=payloads[payload_id])
                        break

    for robot in robots.keys():
        robots[robot].run()

    for station in data.stations.keys():
        data.stations[station].run()
