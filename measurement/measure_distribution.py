import can
import os
import pandas as pd
from can import Message

from jarmuiranyitas_2.measurement.measure import Measure

class MeasurTorque(Measure):
    def __init__(self):
        self.velocity = 0
        self.distribution = 0
        self.yaw_rate = 0
        self.read_previous()


    def update_state_dict(self) -> None:
        yaw = self.imu_measurement()
        velocity, distribution = self.input_signal()
        self.state = (velocity, distribution)
        self.state_dict[self.state] = yaw

    def imu_measurement(self) -> float:
        yaw_rate = 0

        return yaw_rate

    def input_signal(self):
        return self.velocity, self.distribution

    def write_file(self)->None:

        df = pd.DataFrame(self.state_dict)
        df.to_csv(index=False)
        print(df)

    def read_previous(self):
        self.path = os.getcwd()
        self.path = self.path + "/results/torque.xlsx"
        self.state = (self.velocity, self.steering_angle)
        self.state_dict = {self.state: self.yaw_rate}