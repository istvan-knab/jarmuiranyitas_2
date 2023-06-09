# Járműirányítás 2.

<img align="right" width="325" height="75" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/sztaki_logo_kek.png">

`Pelenczei Bálint` </br>
`Knáb István Gellért`</br>
`Máté Kristóf`



![alt text](https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/_DSC6410.jpg)
## Quick description 📋

This repository is the Documentation of a 1:5 4WD-Car. Descriptions of previous projects  can be accessed by the following link : 

https://drive.google.com/drive/folders/1CZQcddJfMFzFaR6hJL0l49vW3KqHnq_u

## Project Documentation 📑

Each library has it's own short description, which is created as a README.md file.

## The vehicle 🚗

The vehicle is a 1:5 scale car mounted with PMSM motors on each wheel ( 4 kW / wheel) . The CAN network consists of four wheels and the servo which will be used as actuators, but there are other modules that can send messages to other nodes like the Power Management Unit. Addressing will be declared in the CAN folder. Each wheel can get different values of velocity and torque depending on the configuration.


## Task ✒️

- Model identification
- Fix servo backlash
- Mathematical description, find correlation between differential drive and turning radius
