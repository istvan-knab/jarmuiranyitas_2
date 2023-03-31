import copy
from time import sleep

from jarmuiranyitas_2.can.network import CANNetwork
from jarmuiranyitas_2.can.internal_states import InternalStates

from jarmuiranyitas_2.can.ids.can_class_ids import CanClassIDs
from jarmuiranyitas_2.can.ids.can_device_ids import CanDeviceIDs
from jarmuiranyitas_2.can.ids.can_message_type_ids import CanMessageTypeIDs

from jarmuiranyitas_2.can.ids.can_power_management_message_ids import CanPowerManagementMessageIDs
from jarmuiranyitas_2.can.ids.can_servo_message_ids import CanServoMessageIDs
from jarmuiranyitas_2.can.ids.can_wheel_drive_message_ids import CanWheelDriveMessageIDs


class StateHandler:

    def __init__(self, can_network: CANNetwork, init_state: InternalStates):
        self.prev_state = init_state
        self.current_state = copy.deepcopy(self.prev_state)

        self.flags = {"idl": False, "drv": False, "ref": False}
        self.update_flags()

        self.ids = self.create_ids()

        self.reference = {"current": 0.0, "velocity": 0.0, "steering_angle": 0.0}

        self.network = can_network

    def check(self):
        if self.prev_state != self.current_state:
            print("State: {}".format(self.current_state))
            self.prev_state = copy.deepcopy(self.current_state)

    def update_flags(self):
        flags_from_network = self.network.get_flags()
        self.flags.update(flags_from_network)

    def get_current_state(self):
        self.check()

        return self.current_state

    def handle_start1(self):
        cmd_vsrv_on_data = [CanPowerManagementMessageIDs.VSRV, CanPowerManagementMessageIDs.ON]
        self.network.send_message(arbitration_id=self.ids["cmd_pm_id"], extended_id=False, data=cmd_vsrv_on_data)
        self.network.sleep(duration_ms=1500)

        cmd_hvdc_on_data = [CanPowerManagementMessageIDs.HVDC, CanPowerManagementMessageIDs.ON]
        self.network.send_message(arbitration_id=self.ids["cmd_pm_id"], extended_id=False, data=cmd_hvdc_on_data)
        self.network.sleep(duration_ms=1500)

        self.update_flags()

        if self.flags["lv"] and self.flags["hv"]:
            self.current_state = InternalStates.START2
        else:
            self.current_state = InternalStates.ERR
            print("Battery is critical/dead")

        return self.current_state

    def handle_start2(self):
        self.network.discover_units()
        self.update_flags()

        if self.flags["dss"] and self.flags["dw1"] and self.flags["dw2"] and self.flags["dw3"] and self.flags["dw4"]:
            self.current_state = InternalStates.START3

        else:
            self.current_state = InternalStates.ERR
            print("Discovery of unit(s) failed")

        return self.current_state

    def handle_start3(self):
        cmd_servo_mode_start_data = [CanServoMessageIDs.MODE, CanServoMessageIDs.MODE_START]
        self.network.send_message(arbitration_id=self.ids["cmd_servo_id"], extended_id=False,
                                  data=cmd_servo_mode_start_data)
        self.network.sleep(duration_ms=100)

        cfg_wd_control_velocity_data = [CanWheelDriveMessageIDs.CONTROL_MODE, 0, 0, 0,
                                        CanWheelDriveMessageIDs.VELOCITY, 0, 0, 0]
        self.network.send_message(arbitration_id=self.ids["cfg_wd_fr_id"], extended_id=False,
                                  data=cfg_wd_control_velocity_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_fl_id"], extended_id=False,
                                  data=cfg_wd_control_velocity_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_rr_id"], extended_id=False,
                                  data=cfg_wd_control_velocity_data)
        self.network.send_message(arbitration_id=self.ids["cfg_wd_rl_id"], extended_id=False,
                                  data=cfg_wd_control_velocity_data)

        self.current_state = InternalStates.IDLE
        self.flags["idl"] = True

        return self.current_state

    def handle_idle(self):
        if self.flags["idl"]:
            cmd_wd_mode_drive_data = [CanWheelDriveMessageIDs.MODE, 0, CanWheelDriveMessageIDs.DRIVE, 0]
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)

            cmd_wd_state_stopped_data = [CanWheelDriveMessageIDs.DRIVE_STATE, 0, CanWheelDriveMessageIDs.STOPPED, 0]
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                      data=cmd_wd_state_stopped_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                      data=cmd_wd_state_stopped_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
                                      data=cmd_wd_state_stopped_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
                                      data=cmd_wd_state_stopped_data)

            self.reference["velocity"] = 0
            self.reference["current"] = 0
            self.reference["steering_angle"] = 0
            self.flags["ref"] = False

        self.flags["idl"] = False

        return self.current_state

    def handle_drive(self):
       
        if self.flags["drv"] :
            self.flags["ref"] = 1

            cmd_wd_mode_drive_data = [CanWheelDriveMessageIDs.MODE, 0, CanWheelDriveMessageIDs.DRIVE, 0]
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
                                      data=cmd_wd_mode_drive_data)

            cmd_wd_state_started_data = [CanWheelDriveMessageIDs.DRIVE_STATE, 0, CanWheelDriveMessageIDs.STARTED, 0]
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fr_id"], extended_id=False,
                                      data=cmd_wd_state_started_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_fl_id"], extended_id=False,
                                      data=cmd_wd_state_started_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_rr_id"], extended_id=False,
                                      data=cmd_wd_state_started_data)
            self.network.send_message(arbitration_id=self.ids["cmd_wd_rl_id"], extended_id=False,
                                      data=cmd_wd_state_started_data)
        self.flags["drv"] = 0
        self.reference["velocity"] = 0
        sleep(5/1000)
        
        return self.current_state

    def handle_err(self):
        # TODO:
        return self.current_state

    def create_ids(self):
        ids = {}

        cmd_pm_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_POWER_MANAGEMENT,
                                                         device_id=CanDeviceIDs.CAN_DEVICE_POWER_MANAGEMENT,
                                                         message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_COMMAND)
        ids["cmd_pm_id"] = cmd_pm_id

        cmd_servo_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_SERVO,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_SERVO,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_COMMAND)
        ids["cmd_Servo_id"] = cmd_servo_id

        cfg_wd_fr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_WHEEL_DRIVE,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_FR,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_CONFIG)
        ids["cfg_wd_fr_id"] = cfg_wd_fr_id

        cfg_wd_fl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_WHEEL_DRIVE,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_FL,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_CONFIG)
        ids["cfg_wd_fl_id"] = cfg_wd_fl_id

        cfg_wd_rl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_WHEEL_DRIVE,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_RL,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_CONFIG)
        ids["cfg_wd_rl_id"] = cfg_wd_rl_id

        cfg_wd_rr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_WHEEL_DRIVE,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_RR,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_CONFIG)
        ids["cfg_wd_rr_id"] = cfg_wd_rr_id

        cmd_wd_fr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_WHEEL_DRIVE,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_FR,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_COMMAND)
        ids["cmd_wd_fr_id"] = cmd_wd_fr_id

        cmd_wd_fl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_WHEEL_DRIVE,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_FL,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_COMMAND)
        ids["cmd_wd_fl_id"] = cmd_wd_fl_id

        cmd_wd_rr_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_WHEEL_DRIVE,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_RR,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_COMMAND)
        ids["cmd_wd_rr_id"] = cmd_wd_rr_id

        cmd_wd_rl_id = self.network.generate_arbitration_id(class_id=CanClassIDs.CAN_CLASS_WHEEL_DRIVE,
                                                            device_id=CanDeviceIDs.CAN_DEVICE_WHEEL_DRIVE_RL,
                                                            message_type_id=CanMessageTypeIDs.CAN_MESSAGE_TYPE_COMMAND)
        ids["cmd_wd_rl_id"] = cmd_wd_rl_id

        return ids
