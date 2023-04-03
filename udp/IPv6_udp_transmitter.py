import socket
from time import sleep
import json
from pprint import pprint


class UDPTransmitter:

    def __init__(self, transmit_to: str = 'Orin', port: int = 5005):
        self.udp_ip = socket.getaddrinfo(transmit_to, port, family=socket.AF_INET6, proto=socket.IPPROTO_UDP)[0][4][0]
        self.udp_port = port
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    def transmit(self, data_dict: dict):
        data_encoded = json.dumps(data_dict).encode('utf-8')
        self.sock.sendto(data_encoded, (self.udp_ip, self.udp_port))
        pprint(data_dict)
        sleep(0.1)
