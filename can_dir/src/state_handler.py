import copy
import struct

from jarmuiranyitas_2.can_dir.src.network import CANNetwork
from jarmuiranyitas_2.can_dir.enums.internal_states import InternalStates

from jarmuiranyitas_2.can_dir.enums.arbitration_ids.can_class_ids import CanClassIDs
from jarmuiranyitas_2.can_dir.enums.arbitration_ids.can_device_ids import CanDeviceIDs
from jarmuiranyitas_2.can_dir.enums.arbitration_ids.can_message_type_ids import CanMessageTypeIDs

from jarmuiranyitas_2.can_dir.enums.message_codes.can_power_management_message_ids import CanPowerManagementMessageIDs
from jarmuiranyitas_2.can_dir.enums.message_codes.can_servo_message_ids import CanServoMessageIDs
from jarmuiranyitas_2.can_dir.enums.message_codes.can_wheel_drive_message_ids import CanWheelDriveMessageIDs

from jarmuiranyitas_2.controllers.torque_controller import Torque
from jarmuiranyitas_2.controllers.ackermann import Ackermann


class StateHandler:

    def __init__(self, can_network: CANNetwork, init_state: InternalStates, controller):
        self.prev_state = init_state
        self.current_state = copy.deepcopy(self.prev_state)

        self.network = can_network
        self.controller = controller

        self.flags = {"idl": False, "drv": False, "ref": False}
        self.update_flags()

        self.ids = self.create_ids()

        self.reference = {"current": [0.0, 0.0, 0.0, 0.0],
                          "velocity": [0.0, 0.0, 0.0, 0.0],
                          "steering_angle": 0.0}

    def check(self):
        if self.prev_state != self.current_state:
            print("State: {}".format(self.current_state))
            self.prev_state = copy.deepcopy(self.current_state)

    def update_flags(self):
        flags_from_network = self.network.get_flags()
        self.flags.update(flags_from_network)

    def set_ref_vals(self, ref_vals: dict):
        self.reference.update(ref_vals)

    def get_current_state(self):
        self.check()

        return self.current_state

    def handle_start1(self):
        cmd_vsrv_on_data = [CanPowerManagementMessageIDs.VSRV.value, CanPowerManagementMessageIDs.ON.value]
        self.network.send_message(arbitration_id=self.ids["cmd_pm_id"], extended_id=False, data=cmd_vsrv_on_data)
        self.network.sleep(duration_ms=1500)

        cmd_hvdc_on_data = [CanPowerManagementMessageIDs.HVDC.value, CanPowerManagementMessageIDs.ON.value]
        self.network.send_message(arbitration_id=self.ids["cmd_pm_id"], extended_id=False, data=cmd_hvdc_on_data)
        self.network.sleep(duration_ms=1500)

        self.update_flags()
        self.network.sleep(duration_ms=100)

        if self.flags["lv"] and self.flags["hv"]:
            self.prev_state = self.current_state
            self.current_state = InternalStates.START2
        else:
            self.prev_state = self.current_state
            self.current_state = InternalStates.ERR
            print("Battery is critical/dead")

        self.network.sleep(duration_ms=100)

        return self.current_state

    def handle_start2(self):
        self.discover_units()
        self.network.sleep(duration_ms=1500)
        self.update_flags()

        #  and self.flags["dw3"] and self.flags["dw4"]
        if self.flags["dss"] and self.flags["dw1"] and self.flags["dw2"]:
            self.prev_state = self.current_state
            self.current_state = InternalStates.START3

        else:
            self.prev_state = self.current_state
            self.current_state = InternalStates.ERR
            print("Discovery of unit(s) failed")

        self.network.sleep(duration_ms=100)

        return self.current_state

    def handle_start3(self):
        cmd_servo_mode_start_data = [CanServoMessageIDs.MODE.value, CanServoMessageIDs.MODE_START.value]
        self.network.send_message(arbitration_id=self.ids["cmd_servo_id"], extended_id=False,
                                  data=cmd_servo_mode_start_data)
        self.network.sleep(duration_ms=100)

        cfg_wd_control_velocity_data = [CanWheelDriveMessageIDs.CONTROL_MODE.value, 0, 0, 0,
                                        CanWheelDriveMessageIDs.VELOCITY.value, 0, 0, 0]
        self.network.send_message(arbitration_id=self.ids["cfg_wd_fr_id"], extended_id=False,
                                  data=cfg_wd_control_velocity_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_fl_id"], extended_id=False,
                                  data=cfg_wd_control_velocity_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_rr_id"], extended_id=False,
                                  data=cfg_wd_control_velocity_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_rl_id"], extended_id=False,
                                  data=cfg_wd_control_velocity_data)

        cfg_wd_torque_limit_max_data = [CanWheelDriveMessageIDs.TORQUE_LIMIT_MAX.value, 0, 0, 0, 0, 64, 28, 70]
        self.network.send_message(arbitration_id=self.ids["cfg_wd_fr_id"], extended_id=False,
                                  data=cfg_wd_torque_limit_max_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_fl_id"], extended_id=False,
                                  data=cfg_wd_torque_limit_max_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_rr_id"], extended_id=False,
                                  data=cfg_wd_torque_limit_max_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_rl_id"], extended_id=False,
                                  data=cfg_wd_torque_limit_max_data)

        cfg_wd_velocity_limit_data = [CanWheelDriveMessageIDs.VELOCITY_LIMIT.value, 0, 0, 0, 0, 64, 28, 70]
        self.network.send_message(arbitration_id=self.ids["cfg_wd_fr_id"], extended_id=False,
                                  data=cfg_wd_velocity_limit_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_fl_id"], extended_id=False,
                                  data=cfg_wd_velocity_limit_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_rr_id"], extended_id=False,
                                  data=cfg_wd_velocity_limit_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_rl_id"], extended_id=False,
                                  data=cfg_wd_velocity_limit_data)

        self.prev_state = self.current_state
        self.current_state = InternalStates.IDLE
        self.flags["idl"] = True

        return self.current_state

    def handle_idle(self):
        if self.flags["idl"]:
            cmd_vsrv_on_data = [CanPowerManagementMessageIDs.VSRV.value, CanPowerManagementMessageIDs.ON.value]
            self.network.send_message(arbitration_id=self.ids["cmd_pm_id"], extended_id=False, data=cmd_vsrv_on_data)
            self.network.sleep(duration_ms=1000)
            cmd_hvdc_on_data = [CanPowerManagementMessageIDs.HVDC.value, CanPowerManagementMessageIDs.ON.value]
            self.network.send_message(arbitration_id=self.ids["cmd_pm_id"], extended_id=False, data=cmd_hvdc_on_data)

            cmd_wd_mode_drive_data = [CanWheelDriveMessageIDs.MODE.value, 0, CanWheelDriveMessageIDs.DRIVE.value, 0]
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            # self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
            #                           data=cmd_wd_mode_drive_data)
            # self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
            #                           data=cmd_wd_mode_drive_data)

            cmd_wd_state_stopped_data = [CanWheelDriveMessageIDs.DRIVE_STATE.value, 0,
                                         CanWheelDriveMessageIDs.STOPPED.value, 0]
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                      data=cmd_wd_state_stopped_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                      data=cmd_wd_state_stopped_data)
            # self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
            #                           data=cmd_wd_state_stopped_data)
            # self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
            #                           data=cmd_wd_state_stopped_data)

            self.reference["velocity"] = [0.0, 0.0, 0.0, 0.0]
            self.reference["current"] = [0.0, 0.0, 0.0, 0.0]
            self.reference["steering_angle"] = 0.0
            self.flags["ref"] = False

        self.flags["idl"] = False

        ####
        self.flags["drv"] = True
        self.prev_state = self.current_state
        self.current_state = InternalStates.DRIVE
        self.network.sleep(duration_ms=1000)
        ####

        return self.current_state

    def handle_drive(self):
        if self.flags["drv"]:
            self.flags["ref"] = True

            cmd_wd_mode_drive_data = [CanWheelDriveMessageIDs.MODE.value, 0, CanWheelDriveMessageIDs.DRIVE.value, 0]
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            # self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
            #                           data=cmd_wd_mode_drive_data)
            # self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
            #                           data=cmd_wd_mode_drive_data)

            cmd_wd_state_started_data = [CanWheelDriveMessageIDs.DRIVE_STATE.value, 0,
                                         CanWheelDriveMessageIDs.STARTED.value, 0]
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                      data=cmd_wd_state_started_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                      data=cmd_wd_state_started_data)
            # self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
            #                           data=cmd_wd_state_started_data)
            # self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
            #                           data=cmd_wd_state_started_data)

            self.flags["drv"] = False

        self.send_reference()
        
        return self.current_state

    def handle_err(self):
        self.flags["ref"] = False
        cmd_servo_state_idle = [CanServoMessageIDs.MODE.value, CanServoMessageIDs.MODE_IDLE.value]
        self.network.send_message(arbitration_id=self.ids["cmd_servo_id"], extended_id=False,
                                  data=cmd_servo_state_idle)

        cmd_wd_state_stopped_data = [CanWheelDriveMessageIDs.DRIVE_STATE.value, 0,
                                     CanWheelDriveMessageIDs.STOPPED.value, 0]
        self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                  data=cmd_wd_state_stopped_data)
        self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                  data=cmd_wd_state_stopped_data)
        self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
                                  data=cmd_wd_state_stopped_data)
        self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
                                  data=cmd_wd_state_stopped_data)

        return self.current_state

    def create_ids(self):
        ids = {}

        cmd_pm_id = self.network.generate_arbitration_id(class_id=CanClassIDs.POWER_MANAGEMENT.value,
                                                         device_id=CanDeviceIDs.POWER_MANAGEMENT.value,
                                                         message_type_id=CanMessageTypeIDs.COMMAND.value)
        ids["cmd_pm_id"] = cmd_pm_id

        cmd_servo_id = self.network.generate_arbitration_id(class_id=CanClassIDs.SERVO.value,
                                                            device_id=CanDeviceIDs.SERVO.value,
                                                            message_type_id=CanMessageTypeIDs.COMMAND.value)
        ids["cmd_servo_id"] = cmd_servo_id

        cfg_wd_fr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_FR.value,
                                                            message_type_id=CanMessageTypeIDs.CONFIG.value)
        ids["cfg_wd_fr_id"] = cfg_wd_fr_id

        cfg_wd_fl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_FL.value,
                                                            message_type_id=CanMessageTypeIDs.CONFIG.value)
        ids["cfg_wd_fl_id"] = cfg_wd_fl_id

        cfg_wd_rl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_RL.value,
                                                            message_type_id=CanMessageTypeIDs.CONFIG.value)
        ids["cfg_wd_rl_id"] = cfg_wd_rl_id

        cfg_wd_rr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_RR.value,
                                                            message_type_id=CanMessageTypeIDs.CONFIG.value)
        ids["cfg_wd_rr_id"] = cfg_wd_rr_id

        cmd_wd_fr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_FR.value,
                                                            message_type_id=CanMessageTypeIDs.COMMAND.value)
        ids["cmd_wd_fr_id"] = cmd_wd_fr_id

        cmd_wd_fl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_FL.value,
                                                            message_type_id=CanMessageTypeIDs.COMMAND.value)
        ids["cmd_wd_fl_id"] = cmd_wd_fl_id

        cmd_wd_rr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_RR.value,
                                                            message_type_id=CanMessageTypeIDs.COMMAND.value)
        ids["cmd_wd_rr_id"] = cmd_wd_rr_id

        cmd_wd_rl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_RL.value,
                                                            message_type_id=CanMessageTypeIDs.COMMAND.value)
        ids["cmd_wd_rl_id"] = cmd_wd_rl_id

        ref_wd_fr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_FR.value,
                                                            message_type_id=CanMessageTypeIDs.REFERENCE.value)
        ids["ref_wd_fr_id"] = ref_wd_fr_id

        ref_wd_fl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_FL.value,
                                                            message_type_id=CanMessageTypeIDs.REFERENCE.value)
        ids["ref_wd_fl_id"] = ref_wd_fl_id

        ref_wd_rl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_RL.value,
                                                            message_type_id=CanMessageTypeIDs.REFERENCE.value)
        ids["ref_wd_rl_id"] = ref_wd_rl_id

        ref_wd_rr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.WHEEL_DRIVE.value,
                                                            device_id=CanDeviceIDs.WHEEL_DRIVE_RR.value,
                                                            message_type_id=CanMessageTypeIDs.REFERENCE.value)
        ids["ref_wd_rr_id"] = ref_wd_rr_id

        ref_servo_id = self.network.generate_arbitration_id(class_id=CanClassIDs.SERVO.value,
                                                            device_id=CanDeviceIDs.SERVO.value,
                                                            message_type_id=CanMessageTypeIDs.REFERENCE.value)
        ids["ref_servo_id"] = ref_servo_id

        return ids

    def discover_units(self):
        cmd_discover_data = [CanWheelDriveMessageIDs.DISCOVER.value, 0]
        self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False, data=cmd_discover_data)
        self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False, data=cmd_discover_data)
        self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False, data=cmd_discover_data)
        self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False, data=cmd_discover_data)
        self.network.send_message(arbitration_id=self.ids["cmd_servo_id"], extended_id=False, data=cmd_discover_data)

    def send_reference(self):
        while True:
            self.network.sleep(duration_ms=100)
            input_vector = {"steering_angle": self.reference["steering_angle"],
                            "velocity": self.reference["velocity"][0] * 100}
            rpm = self.controller.control(input_vector=input_vector)

            ref_wd_fr_data = self.get_wd_reference_msg(self.reference["current"][0], rpm["FR"])
            ref_wd_fl_data = self.get_wd_reference_msg(self.reference["current"][1], rpm["FL"])
            ref_wd_rl_data = self.get_wd_reference_msg(self.reference["current"][2], rpm["RL"])
            ref_wd_rr_data = self.get_wd_reference_msg(self.reference["current"][3], rpm["RR"])
            ref_servo_data = self.get_servo_reference_msg(self.reference["steering_angle"])

            self.network.send_message(arbitration_id=self.ids["ref_wd_fr_id"], extended_id=False, data=ref_wd_fr_data)
            self.network.send_message(arbitration_id=self.ids["ref_wd_fl_id"], extended_id=False, data=ref_wd_fl_data)
            self.network.send_message(arbitration_id=self.ids["ref_wd_rl_id"], extended_id=False, data=ref_wd_rl_data)
            self.network.send_message(arbitration_id=self.ids["ref_wd_rr_id"], extended_id=False, data=ref_wd_rr_data)
            self.network.send_message(arbitration_id=self.ids["ref_servo_id"], extended_id=False, data=ref_servo_data)

    @staticmethod
    def get_wd_reference_msg(current: float, velocity: float):
        data_byte_array_1 = bytearray(struct.pack("<f", current))
        data_byte_array_2 = bytearray(struct.pack("<f", velocity))
        data_list_1 = [data_byte_array_1[i] for i in range(4)]
        data_list_2 = [data_byte_array_2[i] for i in range(4)]
        data_list_1.extend(data_list_2)

        return data_list_1

    @staticmethod
    def get_servo_reference_msg(value: float):
        pos_limit_per_side = 16
        int_value = round(pos_limit_per_side * value)
        if value >= 0:
            bin_value = '{0:016b}'.format(int_value)
        else:
            bin_value = '{0:016b}'.format(0xffff - ~int_value)
        reference_smg_data = [int(bin_value[0:8], 2), int(bin_value[8:16], 2)]

        return reference_smg_data
