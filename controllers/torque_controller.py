import numpy as np


class Torque:

    def __init__(self):
        self.torque_mid = 0.0
        self.output_signal = np.zeros(4)
        self.steering_signal = 0.0
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

    def distribution(self, input_signal: float, steering_signal: float) -> np.array:
        self.input_signal = input_signal * self.pedal_gain
        self.steering_signal = steering_signal * self.input_angle_gain
        for wheel in range(len(self.wheels)):
            self.output_signal[wheel] = self.calculate_torque(wheel=self.wheels[wheel])

        return self.output_signal


    def calculate_torque(self, wheel: str):
        """
        This function will be responsible to calculate the torques by giving
        velocity and wheel id as input
        return:torque
        """
        # default value for debug
        if wheel == "front_right":
            reference_signal = self.input_signal * (1 + self.steering_signal)
        elif wheel == "front_left":
            reference_signal = self.input_signal * (1 - self.steering_signal)
        elif wheel == "rear_right":
            reference_signal = self.input_signal * (1 + self.steering_signal)
        elif wheel == "rear_left":
            reference_signal = self.input_signal * (1 - self.steering_signal)
        else:
            raise Exception("Wrong input")
        return reference_signal
