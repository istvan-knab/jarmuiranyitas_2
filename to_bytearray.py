import struct
#
# value = 5.1
#
# ba = bytearray(struct.pack("f", 16.0))
# print(ba)

import struct

# Define the byte array in hexadecimal format
byte_array_hex = '\xdev\xc3\xb6\xd8\x01\x01\x02'

# Convert the byte array from hexadecimal to binary format
byte_array = bytes.fromhex(byte_array_hex.decode())

# Unpack the binary representation of the float using the 'f' format code
float_value = struct.unpack('f', byte_array)[0]

print(float_value) # Output: 1.6