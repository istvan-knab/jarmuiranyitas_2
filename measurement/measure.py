import can
from can import Message

class Measure:
    """
    This class is the abstraction of measure yaw rate to get function between that and the
    input signal . With measuring that data our goal is to find correlation between steering angle
    and torque distribution by the certain points , and if we have the necessary amount of data,
    we will fit a curve

    The reference yaw rate will be measured by a heat compensated imu ( Inertial Measurement Unit), which
    will log the actual yaw rate by CAN-signals, like the other connections in the car
    """
    def __init__(self):
        self.velocity = 0
        self.control = 0
        self.yaw_rate = 0
        self.state = (self.velocity, self.control)
        self.state_dict = {self.state : self.yaw_rate}

    def update_state_dict(self)->None:
        pass
    def imu_measurement(self)->float:
        pass
    def input_signal(self):
        pass
    def write_file(self):
        pass

