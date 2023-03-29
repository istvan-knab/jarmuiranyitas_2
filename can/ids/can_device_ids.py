from enum import Enum


class CanDeviceIDs(Enum):

    CAN_DEVICE_WHEEL_DRIVE_FR = 0x01
    CAN_DEVICE_WHEEL_DRIVE_FL = 0x02
    CAN_DEVICE_WHEEL_DRIVE_RL = 0x03
    CAN_DEVICE_WHEEL_DRIVE_RR = 0x04
    CAN_DEVICE_POWER_MANAGEMENT = 0x01
    CAN_DEVICE_SERVO = 0x01
