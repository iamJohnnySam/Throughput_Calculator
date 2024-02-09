import json

import data
import logging
from payload import Payload
from robot import Robot

process_time = 22 * 60 * 60
input_every = 12840 / 4
new_payload_id = 0
robots = {1: Robot(1)}
# robots = {1: Robot(1),
#           2: Robot(2)}
payloads = {}


def create_payload(p_id, time):
    payloads[p_id]: Payload = Payload(create=time,
                                      payload_id=p_id,
                                      current_station=data.sequence[0]+"_0")
    logging.log("Payload Created with ID > " + str(p_id))

    data.stations[data.sequence[0]+"_0"].stock.append(payloads[p_id])


new_payload_id = new_payload_id + 1
create_payload(new_payload_id, 0)
new_payload_id = new_payload_id + 1
create_payload(new_payload_id, 0)
new_payload_id = new_payload_id + 1
create_payload(new_payload_id, 0)
new_payload_id = new_payload_id + 1
create_payload(new_payload_id, 0)


for sec in range(process_time):
    logging.log(f"\nTime = {sec}")

    if sec % input_every == 0:
        new_payload_id = new_payload_id + 1
        create_payload(new_payload_id, sec)

    for payload_id in list(payloads.keys()):
        if payloads[payload_id].current_station.split('_')[0] == data.sequence[-1]:
            logging.log(f"------------- PAYLOAD {payload_id} DONE AT {sec} -----------------")
            print(f"------------- PAYLOAD {payload_id} DONE AT {sec} -----------------")
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
