import can
from can import Message
import csv
import pandas as pd
import os
import numpy as np

from jarmuiranyitas_2.measurement.measure import Measure

class MeasureAngle(Measure):
    def __init__(self):
        """
        Three dimensional state, with velocity, steering angle and yaw_rate.
        The function of this class is to find correlation function relationship between this values.
        """
        self.path = os.getcwd()
        self.path = self.path + "/results/steering.csv"
        self.velocity = list()
        self.steering_angle = list()
        self.yaw_rate = list()
        self.write_file()
        self.read_previous()


    def update_state_dict(self) -> None:
        """
        This function is responsible for updating the measured values
        state dict will be saved in the load csv function
        """
        yaw = self.imu_measurement()
        velocity,steering = self.input_signal()
        self.state = (velocity, steering)

    def imu_measurement(self) -> float:

        # get data from imu
        yaw_rate = 2
        return yaw_rate

    def input_signal(self) -> float :

         #get can data
        velocity = 0
         #get can data
        steering= 3

        return velocity, steering

    def write_file(self)->None:

        df = pd.DataFrame({'Velocity': self.velocity,
                           "Steering angle": self.steering_angle,
                           "Yaw": self.yaw_rate
                           })
        df.to_csv(self.path)
        

    def read_previous(self):
        self.path = os.getcwd()
        self.path = self.path + "/results/steering.csv"
        read_data = pd.read_csv(self.path)
        self.velocity = list(read_data["Velocity"])
        self.steering_angle = list(read_data["Steering angle"])
        self.yaw_rate = list(read_data["Yaw"])

        for elements in range(len(self.velocity)):
            self.state[elements] = (self.velocity[elements], self.steering_angle[elements])
            self.state_dict = {self.state: self.yaw_rate}


m = MeasureAngle()
m.write_file()