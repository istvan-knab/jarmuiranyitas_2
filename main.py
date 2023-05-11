import os
import sys
from threading import Thread

PROJECT_DIR = os.path.dirname(os.path.abspath("main.py"))
sys.path.append(os.path.dirname(PROJECT_DIR))

from jarmuiranyitas_2.can_dir.src.can_main import CAN
from jarmuiranyitas_2.udp.IPv6_udp_receiver import UDPReceiver
from jarmuiranyitas_2.measurement.start_measurement import StartMeasurement


def main():
    can = CAN()
    udp = UDPReceiver()
    #todo :implement config
    measure = StartMeasurement("steering",100)

    can_comm = Thread(target=can.start_communication)
    udp_listener = Thread(target=udp.receive)
    cross_comm = Thread(target=can.set_ref_vals, args=[udp.last_data])
    imu_start = Thread(target=measure.active())


    can_comm.start()
    udp_listener.start()
    cross_comm.start()
    imu_start.start()


if __name__ == "__main__":
    main()
