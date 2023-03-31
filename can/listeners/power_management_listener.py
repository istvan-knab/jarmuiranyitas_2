from can import Message

from jarmuiranyitas_2.can.listeners.listener import Listener
from jarmuiranyitas_2.can.ids.can_class_ids import CanClassIDs
from jarmuiranyitas_2.can.ids.can_device_ids import CanDeviceIDs
from jarmuiranyitas_2.can.ids.can_message_type_ids import CanMessageTypeIDs
from jarmuiranyitas_2.can.ids.can_power_management_message_ids import CanPowerManagementMessageIDs


class PowerManagementListener(Listener):
    def __init__(self):
        super(PowerManagementListener, self).__init__()

        self.flag_LV = False
        self.flag_HV = False

        power_management_status_id_bin = f'{CanClassIDs.CAN_CLASS_POWER_MANAGEMENT.value:0>4b}' \
                                         f'{CanDeviceIDs.CAN_DEVICE_POWER_MANAGEMENT.value:0>4b}' \
                                         f'{CanMessageTypeIDs.STATUS.value:0>3b}'
        self.power_management_status_id = int(power_management_status_id_bin, 2)

        power_management_measurement_id_bin = f'{CanClassIDs.CAN_CLASS_POWER_MANAGEMENT.value:0>4b}' \
                                              f'{CanDeviceIDs.CAN_DEVICE_POWER_MANAGEMENT.value:0>4b}' \
                                              f'{CanMessageTypeIDs.MEASUREMENT.value:0>3b}'
        self.power_management_measurement_id = int(power_management_measurement_id_bin, 2)

    def on_message_received(self, msg: Message) -> None:
        if msg.arbitration_id == self.power_management_measurement_id:
            pass

        elif msg.arbitration_id == self.power_management_status_id:
            if msg.data[1] < CanPowerManagementMessageIDs.BATT_CRITICAL.value:
                self.flag_LV = True
            else:
                self.flag_LV = False
            if msg.data[2] < CanPowerManagementMessageIDs.BATT_CRITICAL.value:
                self.flag_HV = True
            else:
                self.flag_HV = False

    def on_error(self, exc: Exception) -> None:
        pass

    def get_flag_lv(self):
        return self.flag_LV

    def get_flag_hv(self):
        return self.flag_HV
