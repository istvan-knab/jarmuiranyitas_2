from jarmuiranyitas_2.can_dir.src.config import Config
from jarmuiranyitas_2.can_dir.src.network import CANNetwork
from jarmuiranyitas_2.can_dir.enums.internal_states import InternalStates
from jarmuiranyitas_2.can_dir.src.state_handler import StateHandler
from jarmuiranyitas_2.controllers.torque_controller import Torque
from jarmuiranyitas_2.controllers.ackermann import Ackermann


class CAN:

    def __init__(self):
        self.config = Config()
        self.network = CANNetwork(interface=self.config.get_interface(),
                                  channel=self.config.get_channel(),
                                  bitrate=self.config.get_bitrate(),
                                  receive_own_messages=self.config.get_receive_own_messages())
        self.controller = Ackermann()
        self.state_handler = StateHandler(can_network=self.network,
                                          init_state=InternalStates.START1,
                                          controller=self.controller)

        self.current_state = self.state_handler.get_current_state()

    def start_communication(self):
        while True:
            if self.current_state == InternalStates.START1:
                self.current_state = self.state_handler.handle_start1()

            elif self.current_state == InternalStates.START2:
                self.current_state = self.state_handler.handle_start2()

            elif self.current_state == InternalStates.START3:
                self.current_state = self.state_handler.handle_start3()

            elif self.current_state == InternalStates.IDLE:
                self.current_state = self.state_handler.handle_idle()

            elif self.current_state == InternalStates.DRIVE:
                self.current_state = self.state_handler.handle_drive()

            elif self.current_state == InternalStates.ERR:
                self.current_state = self.state_handler.handle_err()

            self.state_handler.check()

    def set_ref_vals(self, ref_vals):
        while True:
            self.state_handler.set_ref_vals(ref_vals)
            self.network.sleep(duration_ms=100)
