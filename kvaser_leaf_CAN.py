# import the library
import can
import binascii
import struct
import codecs
from time import sleep


# create a bus instance
# many other interfaces are supported as well (see documentation)
bus = can.Bus(interface='kvaser',
              channel=0,
              receive_own_messages=True)

# send a message
# message = can.Message(arbitration_id=0x708, is_extended_id=True, data=[0x20, 0x01])
# bus.send(message, timeout=0.2)
message = can.Message(arbitration_id=0x708, is_extended_id=True, data=[0x30, 0x01])
bus.send(message, timeout=0.2)
# sleep(1)
message = can.Message(arbitration_id=0x708, is_extended_id=True, data=[0x30, 0x01])
bus.send(message, timeout=0.2)

# CMD mode drive
message = can.Message(arbitration_id=0x588, is_extended_id=True, data=[0x10, 0x12])
bus.send(message, timeout=0.2)
# sleep(1)
# CMD drive state started
message = can.Message(arbitration_id=0x588, is_extended_id=True, data=[0x50, 0x01])
bus.send(message, timeout=0.2)
# sleep(1)
# CFG control mode velocity
message = can.Message(arbitration_id=0x58d, is_extended_id=True, data=[0x01, 0x00, 0x02, 0x00])
bus.send(message, timeout=0.2)
# sleep(1)
# Reference message
message = can.Message(arbitration_id=0x58a, is_extended_id=True, data=[0x00, 0x00, 0x80, 0x0A])
bus.send(message, timeout=0.2)

# Response messages:
# Power management:
# 070b - bc 76 40 a2 d8 01 00 02
# Power status:
# 070c - 00 00 01
