from enum import Enum


class CanPowerManagementMessageIDs(Enum):

    ON = 0x01
    OFF = 0x02
    VSRV = 0x20
    HVDC = 0x30
    NULL = 0x00
