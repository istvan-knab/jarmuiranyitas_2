from enum import Enum


class CanServoMessageIDs(Enum):

    DISCOVER = 0x90
    MODE = 0xBB
    MODE_IDLE = 0xB0
    MODE_START = 0x0B
    NULL_POINT = 0xCC
    MIN_MAX_ANGLE = 0xDD
    KP_POS = 0x11
    KI_POS = 0x22
    KP_VIR = 0x33
    KI_VIR = 0x44
    RESPONSE_PING = 0x6E
    NULL = 0x00
