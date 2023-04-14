import numpy as np

class Ackermann:

    def __init__(self):
        self.wheelbase = 0.56
        self.inner_wheel_track = 0.33
        self.axle_track = 0.5
        self.wheel_diameter = None
        self.steering_angle = None
        self.alpha = None
        self.beta = None
        self.turning_radius = None
        self.steering_angle = None

        if self.steering_angle > 0:
            self.alpha = -0.00001542 * (self.steering_angle**3) -\
                         0.0001613 * (self.steering_angle**2) +\
                         0.4268 * self.steering_angle -\
                         0.03554
            self.beta = np.arctan(self.wheelbase / ((1 / self.steering_angle) / (self.inner_wheel_track / 2)))
            self.turning_radius = (self.wheelbase / np.tan(self.alpha)) - (self.inner_wheel_track / 2)



    def get_velocity_vector(self):
        pass