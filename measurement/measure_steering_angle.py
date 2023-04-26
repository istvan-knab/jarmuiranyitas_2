import spidev

from jarmuiranyitas_2.measurement.measure import Measure

class MeasurAngle(Measure):
    def __init__(self):
        self.velocity = 0
        self.steering_angle = 0
        self.yaw_rate = 0
        self.state = (self.velocity, self.steering_angle)
        self.state_dict = {self.state: self.yaw_rate}
        spi = spidev.SpiDev()

    def update_state_dict(self) -> None:
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


m = MeasurAngle()
m.update_state_dict()