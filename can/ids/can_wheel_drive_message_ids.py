from enum import Enum


class CanWheelDriveMessageIDs(Enum):

    DISCOVER = 0x90
    MODE = 0x10
    IDLE = 0x11
    DRIVE = 0x12
    DRIVE_STATE = 0x50
    STOPPED = 0x00
    STARTED = 0x01
    CONTROL_MODE = 0x01
    TORQUE = 0x01
    VELOCITY = 0x02
    TORQUE_LIMIT_MIN = 0x02
    TORQUE_LIMIT_MAX = 0x03
    VELOCITY_LIMIT = 0x04
    RESPONSE_PING_FR = 0xc6
    RESPONSE_PING_FL = 0x8f
    RESPONSE_PING_RL = 0xd2
    RESPONSE_PING_RR = 0xd8
    NULL = 0x00
