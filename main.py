import data
import logging

process_time = 22 * 60 * 60
input_every = 600
new_payload_id = 0

for sec in range(process_time):
    logging.log(f"\nTime = {sec}")
    print(sec)

    if sec % input_every == 0:
        new_payload_id = new_payload_id + 1
        data.create_payload(sec, new_payload_id)
        data.stations["Loading"].current_capacity.append(new_payload_id)

    for payload_id in data.payloads.keys():
        current_step = data.payloads[payload_id].get_step()
        if current_step == len(data.sequence):
            del data.payloads[payload_id]
            logging.log("PAYLOAD COMPLETE > " + str(payload_id))
            continue

        if data.payloads[payload_id].get_waiting():
            next_station = data.sequence[current_step + 1]
            prev_station = data.sequence[current_step]

            if data.stations[next_station].get_availability():
                data.robot1.pick(sec, payload_id, next_station, prev_station)

    data.robot1.run(sec)
    for station in data.stations.keys():
        data.stations[station].run(sec)
