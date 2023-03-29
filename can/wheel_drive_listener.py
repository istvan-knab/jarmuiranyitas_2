import can
from can import Message

from jarmuiranyitas_2.can.ids.can_class_ids import CanClassIDs
from jarmuiranyitas_2.can.ids.can_device_ids import CanDeviceIDs
from jarmuiranyitas_2.can.ids.can_message_type_ids import CanMessageTypeIDs


class WheelDriveListener(can.Listener):
    def __init__(self):
        super(WheelDriveListener, self).__init__()

        wheel_drive_fr_response_id_bin = f'{CanClassIDs.CAN_CLASS_WHEEL_DRIVE:0>4b}' \
                                         f'{CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_FR:0>4b}' \
                                         f'{CanMessageTypeIDs.CAN_MESSAGE_TYPE_RESPONSE:0>3b}'
        self.wheel_drive_FR_response_id = int(wheel_drive_fr_response_id_bin, 2)

        wheel_drive_fl_response_id_bin = f'{CanClassIDs.CAN_CLASS_WHEEL_DRIVE:0>4b}' \
                                         f'{CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_FL:0>4b}' \
                                         f'{CanMessageTypeIDs.CAN_MESSAGE_TYPE_RESPONSE:0>3b}'
        self.wheel_drive_FL_response_id = int(wheel_drive_fl_response_id_bin, 2)

        wheel_drive_rr_response_id_bin = f'{CanClassIDs.CAN_CLASS_WHEEL_DRIVE:0>4b}' \
                                         f'{CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_RR:0>4b}' \
                                         f'{CanMessageTypeIDs.CAN_MESSAGE_TYPE_RESPONSE:0>3b}'
        self.wheel_drive_RR_response_id = int(wheel_drive_rr_response_id_bin, 2)

        wheel_drive_rl_response_id_bin = f'{CanClassIDs.CAN_CLASS_WHEEL_DRIVE:0>4b}' \
                                         f'{CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_RL:0>4b}' \
                                         f'{CanMessageTypeIDs.CAN_MESSAGE_TYPE_RESPONSE:0>3b}'
        self.wheel_drive_RL_response_id = int(wheel_drive_rl_response_id_bin, 2)

        wheel_drive_fr_measurement_id_bin = f'{CanClassIDs.CAN_CLASS_WHEEL_DRIVE:0>4b}' \
                                            f'{CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_FR:0>4b}' \
                                            f'{CanMessageTypeIDs.CAN_MESSAGE_TYPE_MEASUREMENT:0>3b}'
        self.wheel_drive_FR_measurement_id = int(wheel_drive_fr_measurement_id_bin, 2)

        wheel_drive_fl_measurement_id_bin = f'{CanClassIDs.CAN_CLASS_WHEEL_DRIVE:0>4b}' \
                                            f'{CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_FL:0>4b}' \
                                            f'{CanMessageTypeIDs.CAN_MESSAGE_TYPE_MEASUREMENT:0>3b}'
        self.wheel_drive_FL_measurement_id = int(wheel_drive_fl_measurement_id_bin, 2)

        wheel_drive_rr_measurement_id_bin = f'{CanClassIDs.CAN_CLASS_WHEEL_DRIVE:0>4b}' \
                                            f'{CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_RR:0>4b}' \
                                            f'{CanMessageTypeIDs.CAN_MESSAGE_TYPE_MEASUREMENT:0>3b}'
        self.wheel_drive_RR_measurement_id = int(wheel_drive_rr_measurement_id_bin, 2)

        wheel_drive_rl_measurement_id_bin = f'{CanClassIDs.CAN_CLASS_WHEEL_DRIVE:0>4b}' \
                                            f'{CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_RL:0>4b}' \
                                            f'{CanMessageTypeIDs.CAN_MESSAGE_TYPE_MEASUREMENT:0>3b}'
        self.wheel_drive_RL_measurement_id = int(wheel_drive_rl_measurement_id_bin, 2)

    def on_message_received(self, msg: Message) -> None:
        if msg.arbitration_id == self.wheel_drive_FR_measurement_id:
            pass
        elif msg.arbitration_id == self.wheel_drive_FL_measurement_id:
            pass
        elif msg.arbitration_id == self.wheel_drive_RR_measurement_id:
            pass
        elif msg.arbitration_id == self.wheel_drive_RL_measurement_id:
            pass
        elif msg.arbitration_id == self.wheel_drive_FR_response_id:
            pass
        elif msg.arbitration_id == self.wheel_drive_FL_response_id:
            pass
        elif msg.arbitration_id == self.wheel_drive_RR_response_id:
            pass
        elif msg.arbitration_id == self.wheel_drive_RL_response_id:
            pass

    def on_error(self, exc: Exception) -> None:
        pass
