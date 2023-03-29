import can
from time import sleep


class CANNetwork:

    def __init__(self, interface: str, channel: str, bitrate: int, receive_own_messages: bool):
        self.bus = can.Bus(interface=interface, channel=channel, bitrate=bitrate,
                           receive_own_messages=receive_own_messages)

    def send_message(self, arbitration_id: hex, extended_id: bool, data: list[hex], timeout: float = 0.1):
        message = can.Message(arbitration_id=arbitration_id, is_extended_id=extended_id, data=data)
        self.bus.send(message, timeout=timeout)

    @staticmethod
    def generate_arbitration_id(class_id: hex, device_id: hex, message_type_id: hex):
        arbitration_id = None

        return arbitration_id

    @staticmethod
    def generate_data():
        arbitration_id = None

        return arbitration_id

    @staticmethod
    def sleep(duration_ms):
        sleep(duration_ms/1000)
