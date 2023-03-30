from enum import Enum


class CanPowerManagementMessageIDs(Enum):

    ON = 0x01
    OFF = 0x02
    VSRV = 0x20
    HVDC = 0x30
    BATT_OK = 0x00
    BATT_LOW = 0x01
    BATT_CRITICAL = 0x02
    BATT_DEAD = 0x03
    NULL = 0x00
