from jarmuiranyitas_2.controllers.torque_controller import Torque

if __name__ == '__main__':

    torque = Torque()
    while True:
        ref_torque = float(input("Add reference torque:"))
        steering_angle = float(input("Add angle:"))
        torques = torque.distribution(torque_mid=ref_torque, steering_angle=steering_angle)
        print(torques)