import can
from can import Message
import pandas as pd
import os

from jarmuiranyitas_2.measurement.measure import Measure

class MeasurAngle(Measure):
    def __init__(self):
        """
        Three dimensional state, with velocity, steering angle and yaw_rate.
        The function of this class is to find correlation function relationship between this values.
        """
        self.velocity = 0
        self.steering_angle = 0
        self.yaw_rate = 0
        self.state = (self.velocity, self.steering_angle)
        self.state_dict = {self.state: self.yaw_rate}


    def update_state_dict(self) -> None:
        """
        This function is responsible for updating the measured values
        state dict will be saved in the load csv function
        """
        yaw = self.imu_measurement()
        velocity,steering = self.input_signal()
        self.state = (velocity, steering)
        self.state_dict[self.state] = yaw

    def imu_measurement(self) -> float:
        yaw_rate = 2
        return yaw_rate

    def input_signal(self) -> float :
        velocity = 0
        steering= 3
        return velocity, steering

    def write_file(self)->None:
        path = os.getcwd()
        path = path + "/results"
        df = pd.DataFrame(self.state_dict)
        df.to_csv(index = False)
        print(df)


m = MeasurAngle()
m.update_state_dict()
m.write_file()