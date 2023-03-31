from enum import Enum


class CanMessageTypeIDs(Enum):

    COMMAND = 0x00
    RESPONSE = 0x01
    REFERENCE = 0x02
    MEASUREMENT = 0x03
    STATUS = 0x04
    CONFIG = 0x05
    SPEC = 0x06
