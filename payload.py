import logging


class Payload:
    def __init__(self, create: int, payload_id: int):
        self.created = create
        self.payload_id = payload_id

        self.current_step = 0
        self.completion = False

        self.waiting = True

    def get_id(self):
        return self.payload_id

    def get_step(self):
        return self.current_step

    def get_waiting(self):
        return self.waiting

    def pick_up(self):
        self.waiting = False
        logging.log(f"LOADER > Picked up: " + str(self.payload_id))

    def drop_off(self):
        self.current_step = self.current_step + 1
        logging.log(f"LOADER > Dropped Off: " + str(self.payload_id))

    def ready_to_pick_up(self):
        self.waiting = True
        logging.log(f"LOADER > Ready for Pick up: " + str(self.payload_id))
