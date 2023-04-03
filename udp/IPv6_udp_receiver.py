import socket
import json
from pprint import pprint


class UDPReceiver:

    def __init__(self, receive_from: str = '::', port: int = 5005):
        self.udp_port = port
        self.udp_ip = receive_from
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))

    def receive(self):
        data, address = self.sock.recvfrom(1024)
        pprint(json.loads(data))
