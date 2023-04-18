import math
from control import TransferFunction
import numpy as np
from jarmuiranyitas_2.vehicle_models.model import Model


class KinematicBycicleModel(Model):
    """
    The lateral description of the car can be realized with the bycicle model. It can
    contain several mechanic parameters, like tyre stiffness, but in lack of this knowledge
    we will simply use the kinematic description of this model.
    """
    def __init__(self) -> None:
        self.x = float()
        v = 0
        self.L = 2 #has to be measured
        self.s = TransferFunction.s
        self.A = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        self.b = np.array([[0],[0],[0],[0],[0]])
        self.Y_s = math.pow(v,2)

    def update(self, u:float) -> tuple:
        """
        State space representation, giving back the values x,y,yaw and theta
        """
        state_array = self.A * self.x + self.b * u

    def transfer_function(self,v: float):
        """
        Declaring the transfer function is necessary, because of giving the chance to the
        pid controller to tune our model
        the transfer function is described in document made by Baranyi Márk
        return: Transfer function
        """

        s = self.s
        Y_s = math.pow(v, 2)
        U_s = self.L * s * s
        G_s =  Y_s/U_s

        return G_s

kbm = KinematicBycicleModel()
kbm.transfer_function(9)