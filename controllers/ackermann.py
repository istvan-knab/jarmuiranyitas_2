import numpy as np

from jarmuiranyitas_2.controllers.controller import Controller


class Ackermann(Controller):

    def __init__(self):
        self.wheelbase = 0.57
        self.inner_wheel_track = 0.33
        self.axle_track = 0.5
        self.wheel_radius = 0.17 / 2

        self.steering_angle = None
        self.velocity = None

        self.alpha = None
        self.beta = None
        self.turning_radius = None
        self.radius_vector = {}
        self.velocity_vector = {}
        self.rpm_vector = {}

    def control(self, input_vector: dict):
        self.steering_angle = np.interp(input_vector["steering_angle"], (-1, 1), (np.deg2rad(-16), np.deg2rad(16)))
        self.velocity = input_vector["velocity"]

        if self.steering_angle > 0:
            self.alpha = -0.00001542 * (self.steering_angle ** 3) - 0.0001613 * (self.steering_angle ** 2) + \
                         0.4268 * self.steering_angle - 0.03554
            self.beta = np.arctan(self.wheelbase / ((1 / self.steering_angle) - (self.inner_wheel_track / 2)))
            self.turning_radius = self.wheelbase / np.tan(self.alpha) - (self.inner_wheel_track / 2)

            self.radius_vector["FR"] = (self.turning_radius - self.axle_track / 2) / np.cos(self.beta)
            self.radius_vector["FL"] = (self.turning_radius + self.axle_track / 2) / np.cos(self.alpha)
            self.radius_vector["RR"] = self.turning_radius - self.axle_track / 2
            self.radius_vector["RL"] = self.turning_radius + self.axle_track / 2

            self.velocity_vector["FR"] = self.velocity / self.turning_radius * self.radius_vector["FR"]
            self.velocity_vector["FL"] = self.velocity / self.turning_radius * self.radius_vector["FL"]
            self.velocity_vector["RR"] = self.velocity / self.turning_radius * self.radius_vector["RR"]
            self.velocity_vector["RL"] = self.velocity / self.turning_radius * self.radius_vector["RL"]

        elif self.steering_angle < 0:
            self.alpha = -np.arctan(self.wheelbase / ((1 / abs(self.steering_angle)) / (self.inner_wheel_track / 2)))
            self.beta = -(-0.00001542 * (abs(self.steering_angle) ** 3) - 0.0001613 * (abs(self.steering_angle) ** 2) +
                          0.4268 * abs(self.steering_angle) - 0.03554)
            self.turning_radius = abs((self.wheelbase / np.tan(abs(self.beta))) - (self.inner_wheel_track / 2))

            self.radius_vector["FR"] = (self.turning_radius + self.axle_track / 2) / np.cos(self.beta)
            self.radius_vector["FL"] = (self.turning_radius - self.axle_track / 2) / np.cos(self.alpha)
            self.radius_vector["RR"] = self.turning_radius + self.axle_track / 2
            self.radius_vector["RL"] = self.turning_radius - self.axle_track / 2

            self.velocity_vector["FR"] = self.velocity / self.turning_radius * self.radius_vector["FR"]
            self.velocity_vector["FL"] = self.velocity / self.turning_radius * self.radius_vector["FL"]
            self.velocity_vector["RR"] = self.velocity / self.turning_radius * self.radius_vector["RR"]
            self.velocity_vector["RL"] = self.velocity / self.turning_radius * self.radius_vector["RL"]

        else:
            self.velocity_vector["FR"] = self.velocity
            self.velocity_vector["FL"] = self.velocity
            self.velocity_vector["RR"] = self.velocity
            self.velocity_vector["RL"] = self.velocity

        self.rpm_vector["FR"] = 60 * self.velocity_vector["FR"] / (2 * np.pi * self.wheel_radius)
        self.rpm_vector["FL"] = 60 * self.velocity_vector["FL"] / (2 * np.pi * self.wheel_radius)
        self.rpm_vector["RR"] = 60 * self.velocity_vector["RR"] / (2 * np.pi * self.wheel_radius)
        self.rpm_vector["RL"] = 60 * self.velocity_vector["RL"] / (2 * np.pi * self.wheel_radius)

        return self.rpm_vector
