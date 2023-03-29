from multiprocessing import Process

from jarmuiranyitas_2.can.config import Config
from jarmuiranyitas_2.can.network import CANNetwork
from jarmuiranyitas_2.can.internal_states import InternalStates
from jarmuiranyitas_2.can.state_handler import StateHandler


def main():
    config = Config()
    network = CANNetwork(interface=config.get_interface(), channel=config.get_channel(), bitrate=config.get_bitrate(),
                         receive_own_messages=config.get_receive_own_messages())
    state_handler = StateHandler(can_network=network, init_state=InternalStates.START1)

    current_state = state_handler.get_current_state()

    while True:
        flags = network.get_flags()

        if current_state == InternalStates.START1:
            current_state = state_handler.handle_start1()

        elif current_state == InternalStates.START2:
            current_state = state_handler.handle_start2()

        elif current_state == InternalStates.START3:
            current_state = state_handler.handle_start3()

        elif current_state == InternalStates.IDLE:
            current_state = state_handler.handle_idle()

        elif current_state == InternalStates.DRIVE:
            current_state = state_handler.handle_drive()

        elif current_state == InternalStates.ERR:
            current_state = state_handler.handle_err()


if __name__ == '__main__':
    main()
