import socket
from time import sleep

# UDP_IP = "::1"  # localhost
UDP_IP = "fc94:2469:4cf7:f700:9fee:80cd:b870:95bf"  # Titan
UDP_PORT = 5005
MESSAGE = "Hello, World1!"

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

for i in range(100):
    sock.sendto(("MESSAGE_" + str(i)).encode(), (UDP_IP, UDP_PORT))
    sleep(0.5)
