# Controllers
<img align="right" width="325" height="75" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/sztaki_logo_kek.png">
<img align="left" width="573" height="413" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/Kinematic-model-general-bicycle-model.ppm"></br></br></br></br>


## Vehicle kinematics
The vehicle will be modelled with the kinematic bycicle model, and by measuring the yaw-rate of the certain states our task is to find correlation between the cases steering with the servo or steering with differential torque. As visible, because the substitution of the wheels by one wheel per shaft we won't get wheel torqes back, that is the reason because we have to measure certain data with IMU and try to reproduce the same values with torque distribution.
## State space representation

Instead of using the value of steering angle as input we have the torque distribution as influence in our model. The implementation of that model can't be realized yet, because some physical parameters are still unknown.
<img align="left" width="349" height="102" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/byc_state.jpg"></br></br></br></br>

## Simple distributed torque controller
## PID Controller
