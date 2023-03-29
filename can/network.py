import can
from time import sleep

from jarmuiranyitas_2.can.wheel_drive_listener import WheelDriveListener
from jarmuiranyitas_2.can.servo_listener import ServoListener
from jarmuiranyitas_2.can.power_management_listener import PowerManagementListener


class CANNetwork:

    def __init__(self, interface: str, channel: str, bitrate: int, receive_own_messages: bool):
        self.bus = can.Bus(interface=interface, channel=channel, bitrate=bitrate,
                           receive_own_messages=receive_own_messages)

        self.wheel_drive_listener = WheelDriveListener()
        self.servo_listener = ServoListener()
        self.power_management_listener = PowerManagementListener()

        self.notifier = can.Notifier(bus=self.bus, listeners=[self.wheel_drive_listener, self.servo_listener,
                                                              self.power_management_listener])

    def send_message(self, arbitration_id: hex, extended_id: bool, data: list[hex], timeout: float = 0.1):
        message = can.Message(arbitration_id=arbitration_id, is_extended_id=extended_id, data=data)
        self.bus.send(message, timeout=timeout)

    def get_flags(self):
        flags = {"lv": self.get_flag_lv(),
                 "hv": self.get_flag_hv(),
                 }

        return flags

    def get_flag_lv(self):
        return self.power_management_listener.get_flag_lv()

    def get_flag_hv(self):
        return self.power_management_listener.get_flag_hv()

    @staticmethod
    def generate_arbitration_id(class_id: hex, device_id: hex, message_type_id: hex):
        arbitration_id_bin = f'{class_id}{device_id:0>4b}{message_type_id:0>3b}'
        arbitration_id = int(arbitration_id_bin, 2)

        return arbitration_id

    @staticmethod
    def generate_data():
        arbitration_id = None

        return arbitration_id

    @staticmethod
    def sleep(duration_ms):
        sleep(duration_ms/1000)
