from jarmuiranyitas_2.vehicle_models.model import Model


class KinematicBycicleModel(Model):
    """
    The lateral description of the car can be realized with the bycicle model. It can
    contain several mechanic parameters, like tyre stiffness, but in lack of this knowledge
    we will simply use the kinematic description of this model.
    """
    def __init__(self) -> None:
        self.x = float()
        self.y = float()
        self.yaw = float()
        self.v = float()
        self.omega = float()
        self.steering_angle = float()
    def update(self) -> tuple:
        """
        State space representation, giving back the values x,y,yaw and theta
        """
        
    def transfer_function(self):
        """
        Declaring the transfer function is necessary, because of giving the chance to the
        pid controller to tune our model
        """
        pass