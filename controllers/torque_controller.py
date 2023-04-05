import numpy as np
class Torque:
    def __init__(self):
        self.center_velocity = 0.0
        self.wheel_torque = np.zeros(4)
        print(self.wheel_torque)

    def get_torque(self, wheel: int)-> float:
        #TODO: Call the torque listener
        pass

    def set_torque(self, wheel: int)-> None:
        self.convert_to_hexa_array()
        #TODO: Send to can bus

    def distribution(self, center_velocity: float, steering_radius: float)-> list:
        self.center_velocity = center_velocity
        for wheel in range(4):
            self.wheel_torque[wheel] = self.calculate_torque(0x01)


    def convert_to_hexa_array(self, control_input :float):
        #TODO: Implement this function
        pass

    def calculate_torque(self, wheel: int):
        """
        This function will be responsible to calculate the torques by giving
        velocity and wheel id as input
        return:torque
        """
        #default value for debug
        torque = 5.2
        return torque


