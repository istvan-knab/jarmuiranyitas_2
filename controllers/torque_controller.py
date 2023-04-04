class Torque:
    def __init__(self):
        self.center_velocity = 0.0

    def get_torque(self, wheel: int)-> float:
        pass

    def set_torque(self, wheel: int)-> None:
        pass

    def distribution(self, center_velocity: float, steering_radius: float)-> list:
        self.center_velocity = center_velocity
        pass

    def calculate_torque(self, wheel: int):
        """
        This function will be responsible to calculate the torques by giving
        velocity and wheel id as input
        return:torque
        """
        return torque
