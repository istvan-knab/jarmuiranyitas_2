import socket
import json
from time import sleep


class UDPReceiver:

    def __init__(self, receive_from: str = '::', port: int = 5005):
        self.udp_port = port
        self.udp_ip = socket.getaddrinfo(receive_from, port, family=socket.AF_INET6, proto=socket.IPPROTO_UDP)[0][4][0]
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))

        self.last_data = {"steering_angle": 0.0,
                          "current": [0.0, 0.0, 0.0, 0.0],
                          "velocity": [0.0, 0.0, 0.0, 0.0],
                          }

    def receive(self):
        while True:
            encoded_data, address = self.sock.recvfrom(1024)
            decoded_data = json.loads(encoded_data)

            self.last_data.update(decoded_data)
