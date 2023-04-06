import struct
import can
from can import Message
from collections import namedtuple


class Listener(can.Listener):

    MEASUREMENT_WHEEL_DRIVE = namedtuple("MeasurementWheelDrive", ("current", "velocity"))
    MEASUREMENT_SERVO = namedtuple("MeasurementServo", ("angle_val", "vir_val", "rpm_val"))
    MEASUREMENT_POWER_MANAGEMENT = namedtuple("MeasurementPowerManagement", ("flags", "hv_batt_state"))
    MEASUREMENT_POWER_MANAGEMENT_FLAGS = namedtuple("MeasurementPowerManagementFlags",
                                                    ("main_switch", "vsrv", "hv_charging", "hv_brake"))

    @staticmethod
    def byte_array_to_float(byte_array_representation):
        float_representation = struct.unpack('<f', byte_array_representation)

        return float_representation

    def on_message_received(self, msg: Message) -> None:
        pass

    def on_error(self, exc: Exception) -> None:
        pass
