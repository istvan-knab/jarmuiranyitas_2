# Járműirányítás 2.

<img align="right" width="325" height="75" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/sztaki_logo_kek.png">

* Pelenczei Bálint
* Knáb István Gellért
* Máté Kristóf



![alt text](https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/_DSC6410.jpg)
## Quick description 📋

This repository is the Documentation of a 1:5 4WD-Car. Descriptions and CAN protocols are declared in the repository of previous projects, which can be accessed by the following link : 

https://drive.google.com/drive/folders/1CZQcddJfMFzFaR6hJL0l49vW3KqHnq_u

## The vehicle 🚗

The vehicle is a 1:5 scale car mounted with PMSM motors on each wheel. The CAN network consists of four wheels and the servo which will be used as actuators, but there are other modules that can send messages to other nodes like the Power Management Unit. Addressing will be declared in the CAN folder. Each wheel can get different values of velocity and torque depending on the configuration.

## Task ✒️

The first task is to realize steering without giving any commands to the servo, only using torque vectoring.
