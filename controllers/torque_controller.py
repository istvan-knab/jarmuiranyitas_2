import numpy as np


class Torque:

    def __init__(self):
        self.torque_mid = 0.0
        self.wheel_torque = np.zeros(4)
        self.steering_angle = 0.0
        self.pedal_gain = 1
        self.input_angle_gain = 0.1
        self.wheels = ("front_right", "front_left", "rear_right", "rear_left")
        print(self.wheel_torque)

    def get_torque(self, wheel: int) -> float:
        """
        By calling this function we can get the actual torque values back
        """
        # TODO: Call the torque listener
        pass

    def distribution(self, torque_mid: float, steering_angle: float) -> np.array:
        self.torque_mid = torque_mid * self.pedal_gain
        self.steering_angle = steering_angle * self.input_angle_gain
        for wheel in range(len(self.wheels)):
            self.wheel_torque[wheel] = self.calculate_torque(wheel=self.wheels[wheel])

        return self.wheel_torque


    def calculate_torque(self, wheel: str):
        """
        This function will be responsible to calculate the torques by giving
        velocity and wheel id as input
        return:torque
        """
        # default value for debug
        if wheel == "front_right":
            torque = self.torque_mid * (1 + self.steering_angle)
        elif wheel == "front_left":
            torque = self.torque_mid * (1 - self.steering_angle)
        elif wheel == "rear_right":
            torque = self.torque_mid * (1 + self.steering_angle)
        elif wheel == "rear_left":
            torque = self.torque_mid * (1 - self.steering_angle)
        else:
            raise Exception("Wrong input")
        return torque
