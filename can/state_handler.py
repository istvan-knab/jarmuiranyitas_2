import copy

from jarmuiranyitas_2.can.network import CANNetwork
from jarmuiranyitas_2.can.internal_states import InternalStates

from jarmuiranyitas_2.can.ids.can_class_ids import CanClassIDs
from jarmuiranyitas_2.can.ids.can_device_ids import CanDeviceIDs
from jarmuiranyitas_2.can.ids.can_message_type_ids import CanMessageTypeIDs

from jarmuiranyitas_2.can.ids.can_power_management_message_ids import CanPowerManagementMessageIDs


class StateHandler:

    def __init__(self, can_network: CANNetwork, init_state: InternalStates):
        self.prev_state = init_state
        self.current_state = copy.deepcopy(self.prev_state)

        self.network = can_network

    def check(self):
        if self.prev_state != self.current_state:
            print("State: {}".format(self.current_state))
            self.prev_state = copy.deepcopy(self.current_state)

    def get_current_state(self):
        self.check()

        return self.current_state

    def handle_start1(self):
        cmd_pm_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_POWER_MANAGEMENT,
                                                         device_id=CanDeviceIDs.CAN_DEVICE_POWER_MANAGEMENT,
                                                         message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_COMMAND)

        cmd_vsrv_on_data = [CanPowerManagementMessageIDs.VSRV, CanPowerManagementMessageIDs.ON]
        self.network.send_message(arbitration_id=cmd_pm_id, extended_id=False, data=cmd_vsrv_on_data)

        cmd_hvdc_on_data = [CanPowerManagementMessageIDs.HVDC, CanPowerManagementMessageIDs.ON]
        self.network.send_message(arbitration_id=cmd_pm_id, extended_id=False, data=cmd_hvdc_on_data)

        return self.current_state

    def handle_start2(self):
        return self.current_state

    def handle_start3(self):
        return self.current_state

    def handle_idle(self):
        return self.current_state

    def handle_drive(self):
        return self.current_state

    def handle_err(self):
        return self.current_state
