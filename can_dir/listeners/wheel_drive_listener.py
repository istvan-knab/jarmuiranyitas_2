from can import Message

from jarmuiranyitas_2.can_dir.listeners.listener import Listener
from jarmuiranyitas_2.can_dir.enums.arbitration_ids.can_class_ids import CanClassIDs
from jarmuiranyitas_2.can_dir.enums.arbitration_ids.can_device_ids import CanDeviceIDs
from jarmuiranyitas_2.can_dir.enums.arbitration_ids.can_message_type_ids import CanMessageTypeIDs
from jarmuiranyitas_2.can_dir.enums.message_codes.can_wheel_drive_message_ids import CanWheelDriveMessageIDs


class WheelDriveListener(Listener):

    def __init__(self):
        super(WheelDriveListener, self).__init__()

        self.flag_dw1 = False
        self.flag_dw2 = False
        self.flag_dw3 = False
        self.flag_dw4 = False

        self.measurement_FR = self.MEASUREMENT_WHEEL_DRIVE
        self.measurement_FL = self.MEASUREMENT_WHEEL_DRIVE
        self.measurement_RL = self.MEASUREMENT_WHEEL_DRIVE
        self.measurement_RR = self.MEASUREMENT_WHEEL_DRIVE

        wheel_drive_fr_response_id_bin = f'{CanClassIDs.WHEEL_DRIVE.value:0>4b}' \
                                         f'{CanDeviceIDs.WHEEL_DRIVE_FR.value:0>4b}' \
                                         f'{CanMessageTypeIDs.RESPONSE.value:0>3b}'
        self.wheel_drive_FR_response_id = int(wheel_drive_fr_response_id_bin, 2)

        wheel_drive_fl_response_id_bin = f'{CanClassIDs.WHEEL_DRIVE.value:0>4b}' \
                                         f'{CanDeviceIDs.WHEEL_DRIVE_FL.value:0>4b}' \
                                         f'{CanMessageTypeIDs.RESPONSE.value:0>3b}'
        self.wheel_drive_FL_response_id = int(wheel_drive_fl_response_id_bin, 2)

        wheel_drive_rr_response_id_bin = f'{CanClassIDs.WHEEL_DRIVE.value:0>4b}' \
                                         f'{CanDeviceIDs.WHEEL_DRIVE_RR.value:0>4b}' \
                                         f'{CanMessageTypeIDs.RESPONSE.value:0>3b}'
        self.wheel_drive_RR_response_id = int(wheel_drive_rr_response_id_bin, 2)

        wheel_drive_rl_response_id_bin = f'{CanClassIDs.WHEEL_DRIVE.value:0>4b}' \
                                         f'{CanDeviceIDs.WHEEL_DRIVE_RL.value:0>4b}' \
                                         f'{CanMessageTypeIDs.RESPONSE.value:0>3b}'
        self.wheel_drive_RL_response_id = int(wheel_drive_rl_response_id_bin, 2)

        wheel_drive_fr_measurement_id_bin = f'{CanClassIDs.WHEEL_DRIVE.value:0>4b}' \
                                            f'{CanDeviceIDs.WHEEL_DRIVE_FR.value:0>4b}' \
                                            f'{CanMessageTypeIDs.MEASUREMENT.value:0>3b}'
        self.wheel_drive_FR_measurement_id = int(wheel_drive_fr_measurement_id_bin, 2)

        wheel_drive_fl_measurement_id_bin = f'{CanClassIDs.WHEEL_DRIVE.value:0>4b}' \
                                            f'{CanDeviceIDs.WHEEL_DRIVE_FL.value:0>4b}' \
                                            f'{CanMessageTypeIDs.MEASUREMENT.value:0>3b}'
        self.wheel_drive_FL_measurement_id = int(wheel_drive_fl_measurement_id_bin, 2)

        wheel_drive_rr_measurement_id_bin = f'{CanClassIDs.WHEEL_DRIVE.value:0>4b}' \
                                            f'{CanDeviceIDs.WHEEL_DRIVE_RR.value:0>4b}' \
                                            f'{CanMessageTypeIDs.MEASUREMENT.value:0>3b}'
        self.wheel_drive_RR_measurement_id = int(wheel_drive_rr_measurement_id_bin, 2)

        wheel_drive_rl_measurement_id_bin = f'{CanClassIDs.WHEEL_DRIVE.value:0>4b}' \
                                            f'{CanDeviceIDs.WHEEL_DRIVE_RL.value:0>4b}' \
                                            f'{CanMessageTypeIDs.MEASUREMENT.value:0>3b}'
        self.wheel_drive_RL_measurement_id = int(wheel_drive_rl_measurement_id_bin, 2)

    def on_message_received(self, msg: Message) -> None:
        if msg.arbitration_id == self.wheel_drive_FR_measurement_id:
            self.measurement_FR.current = self.byte_array_to_float(msg.data[0:4])
            self.measurement_FR.velocity = self.byte_array_to_float(msg.data[4:-1])

        elif msg.arbitration_id == self.wheel_drive_FL_measurement_id:
            self.measurement_FL.current = self.byte_array_to_float(msg.data[0:4])
            self.measurement_FL.velocity = self.byte_array_to_float(msg.data[4:-1])

        elif msg.arbitration_id == self.wheel_drive_RR_measurement_id:
            self.measurement_RR.current = self.byte_array_to_float(msg.data[0:4])
            self.measurement_RR.velocity = self.byte_array_to_float(msg.data[4:-1])

        elif msg.arbitration_id == self.wheel_drive_RL_measurement_id:
            self.measurement_RL.current = self.byte_array_to_float(msg.data[0:4])
            self.measurement_RL.velocity = self.byte_array_to_float(msg.data[4:-1])

        elif msg.arbitration_id == self.wheel_drive_FR_response_id:
            if msg.data[0] == CanWheelDriveMessageIDs.RESPONSE_PING_FR.value:
                self.flag_dw1 = True
            else:
                self.flag_dw1 = False

        elif msg.arbitration_id == self.wheel_drive_FL_response_id:
            if msg.data[0] == CanWheelDriveMessageIDs.RESPONSE_PING_FL.value:
                self.flag_dw2 = True
            else:
                self.flag_dw2 = False

        elif msg.arbitration_id == self.wheel_drive_RL_response_id:
            if msg.data[0] == CanWheelDriveMessageIDs.RESPONSE_PING_RL.value:
                self.flag_dw3 = True
            else:
                self.flag_dw3 = False

        elif msg.arbitration_id == self.wheel_drive_RR_response_id:
            if msg.data[0] == CanWheelDriveMessageIDs.RESPONSE_PING_RR.value:
                self.flag_dw4 = True
            else:
                self.flag_dw4 = False

    def on_error(self, exc: Exception) -> None:
        pass

    def get_flag_dw1(self):
        return self.flag_dw1

    def get_flag_dw2(self):
        return self.flag_dw2

    def get_flag_dw3(self):
        return self.flag_dw3

    def get_flag_dw4(self):
        return self.flag_dw4

    def get_measurement_fr(self):
        return self.measurement_FR

    def get_measurement_fl(self):
        return self.measurement_FL

    def get_measurement_rr(self):
        return self.measurement_RR

    def get_measurement_rl(self):
        return self.measurement_RL
