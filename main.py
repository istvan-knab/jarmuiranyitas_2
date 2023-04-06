import os
import sys
from multiprocessing import Process

PROJECT_DIR = os.path.dirname(os.path.abspath("main.py"))
sys.path.append(os.path.dirname(PROJECT_DIR))

from jarmuiranyitas_2.can_dir.can_main import CAN
from jarmuiranyitas_2.udp.IPv6_udp_receiver import UDPReceiver


def main():
    can = CAN()
    udp = UDPReceiver()

    can_comm = Process(target=can.start_communication)
    udp_listener = Process(target=udp.receive)

    can_comm.start()
    udp_listener.start()

    while True:
        can.set_ref_vals(udp.last_data)


if __name__ == "__main__":
    main()
