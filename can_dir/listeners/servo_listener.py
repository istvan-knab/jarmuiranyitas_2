import can
from can import Message

from jarmuiranyitas_2.can_dir.enums.can_class_ids import CanClassIDs
from jarmuiranyitas_2.can_dir.enums.can_device_ids import CanDeviceIDs
from jarmuiranyitas_2.can_dir.enums.can_message_type_ids import CanMessageTypeIDs
from jarmuiranyitas_2.can_dir.enums.can_servo_message_ids import CanServoMessageIDs


class ServoListener(can.Listener):

    def __init__(self):
        super(ServoListener, self).__init__()

        self.flag_dss = False

        servo_measurement_id_bin = f'{CanClassIDs.SERVO.value:0>4b}' \
                                   f'{CanDeviceIDs.SERVO.value:0>4b}' \
                                   f'{CanMessageTypeIDs.MEASUREMENT.value:0>3b}'
        self.servo_measurement_id = int(servo_measurement_id_bin, 2)

        servo_response_id_bin = f'{CanClassIDs.SERVO.value:0>4b}' \
                                f'{CanDeviceIDs.SERVO.value:0>4b}' \
                                f'{CanMessageTypeIDs.RESPONSE.value:0>3b}'
        self.servo_response_id = int(servo_response_id_bin, 2)

        servo_status_id_bin = f'{CanClassIDs.SERVO.value:0>4b}' \
                              f'{CanDeviceIDs.SERVO.value:0>4b}' \
                              f'{CanMessageTypeIDs.STATUS.value:0>3b}'
        self.servo_status_id = int(servo_status_id_bin, 2)

    def on_message_received(self, msg: Message) -> None:
        if msg.arbitration_id == self.servo_measurement_id:
            pass

        elif msg.arbitration_id == self.servo_status_id:
            pass

        elif msg.arbitration_id == self.servo_response_id:
            if msg.data[0] == CanServoMessageIDs.RESPONSE_PING.value:
                self.flag_dss = True
            else:
                self.flag_dss = False

    def on_error(self, exc: Exception) -> None:
        pass

    def get_flag_dss(self):
        return self.flag_dss
