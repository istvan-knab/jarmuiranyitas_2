import socket
from time import sleep
import json
from pprint import pprint

connect_to = "Titan"

UDP_PORT = 5005
UDP_IP = socket.getaddrinfo(connect_to, UDP_PORT, family=socket.AF_INET6, proto=socket.IPPROTO_UDP)[0][4][0]
# UDP_IP = "::1"  # localhost

sample_dict = {
    "wheel": 31,        # [-1;1]
    "throttle": 0,      # [0;1]
    "brake": 0          # [0;1]
}

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

for i in range(500):
    sample_dict["wheel"] = i
    sample_dict["brake"] = 500 - 10.111 * i

    encode_data = json.dumps(sample_dict).encode('utf-8')

    sock.sendto(encode_data, (UDP_IP, UDP_PORT))
    pprint(sample_dict)
    sleep(1)
