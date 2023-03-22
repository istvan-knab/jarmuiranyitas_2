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
message = can.Message(arbitration_id=0x708, is_extended_id=True, data=[0x20, 0x01])
bus.send(message, timeout=0.2)

sleep(1)
message = can.Message(arbitration_id=0x708, is_extended_id=True, data=[0x30, 0x01])
bus.send(message, timeout=0.2)



# iterate over received messages
for msg in bus:
    # print(f"{msg.arbitration_id:X}: {codecs.decode(msg.data, 'hex_codec')}")
    print(msg)
# or use an asynchronous notifier
notifier = can.Notifier(bus, [can.Logger("recorded.log"), can.Printer()])
