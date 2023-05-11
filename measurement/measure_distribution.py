import can
import os
import pandas as pd
from can import Message
import csv
import random

from jarmuiranyitas_2.measurement.measure import Measure

class MeasureTorque(Measure):
    def __init__(self):
        self.velocity = 0
        self.distribution = 0
        self.yaw_rate = 0
        self.read_previous()
        self.state_dict = {}


    def update_state_dict(self) -> None:
        yaw = self.imu_measurement()
        velocity, distribution = self.input_signal()
        self.state = (velocity, distribution)
        self.state_dict[self.state] = yaw

    def imu_measurement(self) -> float:
        self.yaw_rate = self.yaw_rate + 1
        return self.yaw_rate

    def input_signal(self):
        self.velocity = self.velocity + 1
        self.distribution = self.distribution + 1
        return self.velocity, self.distribution

    def write_file(self)->None:

        df = pd.DataFrame({'Velocity': self.state_dict,
                           "Distribution": self.distribution,
                           "Yaw": self.yaw_rate
                           })
        df.to_csv(self.path)


    def read_previous(self):
        self.path = os.getcwd()
        self.path = self.path + "/results/distribution.csv"
        read_data = pd.read_csv(self.path)
        self.velocity_list = list(read_data["Velocity"])
        self.distribution_list = list(read_data["Distribution"])
        self.yaw = list(read_data["Yaw"])
        self.state = []

        for elements in range(len(self.velocity_list)):
            self.state[elements] = (self.velocity_list[elements], self.distribution_list[elements])
            self.state_dict = {self.state: self.yaw}
