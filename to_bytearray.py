import struct
#
# value = 5.1
#
# ba = bytearray(struct.pack("f", 16.0))
# print(ba)

hex = "\0xbc\0x76\0x40\0xa2\0xd8\0x01\0x00\0x02"

print(float.fromhex(hex))