import can
from time import sleep


class Can:
    def __init__(self):
        self.bus = can.Bus(interface='kvaser', channel=0, receive_own_messages=True, bitrate=500000)
        self.start_sequence()

    def start_sequence(self):
        message = can.Message(arbitration_id=0x708, is_extended_id=False, data=[0x20, 0x01])
        self.bus.send(message, timeout=0.2)
        message = can.Message(arbitration_id=0x708, is_extended_id=False, data=[0x30, 0x01])
        self.bus.send(message, timeout=0.2)
        sleep(1)

        # CMD mode drive
        message = can.Message(arbitration_id=0x588, is_extended_id=False, data=[0x10, 0x00, 0x12, 0x00])
        self.bus.send(message, timeout=0.2)

        # CMD mode drive
        message = can.Message(arbitration_id=0x590, is_extended_id=False, data=[0x10, 0x00, 0x12, 0x00])
        self.bus.send(message, timeout=0.2)

        # CMD mode drive
        message = can.Message(arbitration_id=0x598, is_extended_id=False, data=[0x10, 0x00, 0x12, 0x00])
        self.bus.send(message, timeout=0.2)

        # CMD mode drive
        message = can.Message(arbitration_id=0x5A0, is_extended_id=False, data=[0x10, 0x00, 0x12, 0x00])
        self.bus.send(message, timeout=0.2)

    def servo_steering(self):

        message = can.Message(arbitration_id=0x68a, is_extended_id=False, data=[0x76, 0x30])
        self.bus.send(message, timeout=0.2)

    def start_motors(self):

        self.cmd_drive()
        sleep(0.1)
        message = can.Message(arbitration_id=0x58D, is_extended_id=False, data=[0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00])
        self.bus.send(message, timeout=0.2)
        sleep(0.1)
        message = can.Message(arbitration_id=0x595, is_extended_id=False, data=[0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00])
        self.bus.send(message, timeout=0.2)
        sleep(0.1)
        message = can.Message(arbitration_id=0x59D, is_extended_id=False, data=[0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00])
        self.bus.send(message, timeout=0.2)
        sleep(0.1)
        message = can.Message(arbitration_id=0x5A5, is_extended_id=False, data=[0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00])
        self.bus.send(message, timeout=0.2)
        sleep(0.1)
        message = can.Message(arbitration_id=0x58D, is_extended_id=False, data=[0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x44])
        self.bus.send(message, timeout=0.2)
        sleep(0.1)
        message = can.Message(arbitration_id=0x595, is_extended_id=False, data=[0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x44])
        self.bus.send(message, timeout=0.2)
        sleep(0.1)
        message = can.Message(arbitration_id=0x59D, is_extended_id=False, data=[0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x44])
        self.bus.send(message, timeout=0.2)
        sleep(0.1)
        message = can.Message(arbitration_id=0x5A5, is_extended_id=False, data=[0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x44])
        self.bus.send(message, timeout=0.2)

    def cmd_drive(self):


        # CMD drive state started
        message = can.Message(arbitration_id=0x588, is_extended_id=False, data=[0x50, 0x00, 0x01, 0x00])
        self.bus.send(message, timeout=0.2)


        # CMD drive state started
        message = can.Message(arbitration_id=0x590, is_extended_id=False, data=[0x50, 0x00, 0x01, 0x00])
        self.bus.send(message, timeout=0.2)


        # CMD drive state started
        message = can.Message(arbitration_id=0x598, is_extended_id=False, data=[0x50, 0x00, 0x01, 0x00])
        self.bus.send(message, timeout=0.2)


        # CMD drive state started
        message = can.Message(arbitration_id=0x5A0, is_extended_id=False, data=[0x50, 0x00, 0x01, 0x00])
        self.bus.send(message, timeout=0.2)

    def drive(self):
        while True:
            sleep(0.1)
            message = can.Message(arbitration_id=0x58A, is_extended_id=False,
                                  data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x44])
            self.bus.send(message, timeout=0.2)

            message = can.Message(arbitration_id=0x592, is_extended_id=False,
                                  data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x44])
            self.bus.send(message, timeout=0.2)

            message = can.Message(arbitration_id=0x59A, is_extended_id=False,
                                  data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x44])
            self.bus.send(message, timeout=0.2)

            message = can.Message(arbitration_id=0x5A2, is_extended_id=False,
                                  data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x7a, 0x44])
            self.bus.send(message, timeout=0.2)