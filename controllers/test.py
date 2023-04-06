from jarmuiranyitas_2.controllers.torque_controller import Torque

if __name__ == '__main__':

    torque = Torque()
    while True:
        velocity = float(input("Add vel:"))
        steering_angle = float(input("Add angle:"))
        torques = torque.distribution(torque_mid=velocity, steering_angle=steering_angle)
        print(torques)