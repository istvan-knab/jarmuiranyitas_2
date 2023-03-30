import can

bus = can.Bus(interface='kvaser', channel=0, receive_own_messages=True, bitrate=500000)

# CFG control mode velocity
message = can.Message(arbitration_id=0x58D, is_extended_id=True, data=[0x01, 0x00, 0x02, 0x00])
bus.send(message, timeout=0.2)

# CFG control mode velocity
message = can.Message(arbitration_id=0x595, is_extended_id=True, data=[0x01, 0x00, 0x02, 0x00])
bus.send(message, timeout=0.2)

# CFG control mode velocity
message = can.Message(arbitration_id=0x59D, is_extended_id=True, data=[0x01, 0x00, 0x02, 0x00])
bus.send(message, timeout=0.2)

# CFG control mode velocity
message = can.Message(arbitration_id=0x5A5, is_extended_id=True, data=[0x01, 0x00, 0x02, 0x00])
bus.send(message, timeout=0.2)

message = can.Message(arbitration_id=0x592, is_extended_id=False,
                      data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x80, 0x3f])
bus.send(message, timeout=0.2)

message = can.Message(arbitration_id=0x58A, is_extended_id=False,
                      data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x41])
bus.send(message, timeout=0.2)

message = can.Message(arbitration_id=0x59A, is_extended_id=False,
                      data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xc8, 0x42])
bus.send(message, timeout=0.2)

message = can.Message(arbitration_id=0x5A2, is_extended_id=False,
                      data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x7A, 0x44])
bus.send(message, timeout=0.2)
