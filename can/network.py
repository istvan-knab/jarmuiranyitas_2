import can
from time import sleep

from jarmuiranyitas_2.can.listeners.wheel_drive_listener import WheelDriveListener
from jarmuiranyitas_2.can.listeners.servo_listener import ServoListener
from jarmuiranyitas_2.can.listeners.power_management_listener import PowerManagementListener


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
        flags = {"lv": self.power_management_listener.get_flag_lv(),
                 "hv": self.power_management_listener.get_flag_hv(),
                 "dss": self.servo_listener.get_flag_dss(),
                 "dw1": self.wheel_drive_listener.get_flag_dw1(),
                 "dw2": self.wheel_drive_listener.get_flag_dw2(),
                 "dw3": self.wheel_drive_listener.get_flag_dw3(),
                 "dw4": self.wheel_drive_listener.get_flag_dw4(),
                 }

        return flags

    @staticmethod
    def generate_arbitration_id(class_id: int, device_id: int, message_type_id: int):
        arbitration_id_bin = f'{class_id:0>4b}{device_id:0>4b}{message_type_id:0>3b}'
        arbitration_id = int(arbitration_id_bin, 2)

        return arbitration_id

    @staticmethod
    def generate_data():
        arbitration_id = None

        return arbitration_id

    @staticmethod
    def sleep(duration_ms):
        sleep(duration_ms/1000)
