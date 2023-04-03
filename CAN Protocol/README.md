# CAN protocol 📑

<img align="right" width="325" height="75" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/sztaki_logo_kek.png">

CAN is a vehicle communication protocol, which is developed by Bosch. The idea behind that framework is to realize a master-slave communication through a bus, and with adressing certain Nodes give commands or get network diagnostics. Each frame contains an arbitration field, a DLC field(Data length counter), and the data field which has to be declared if we would like to communicate. The data will be sent in hexadecimal arrays, with maximal byte length of 8. We won't use the extended data, only the standard CAN Frame length.

<img align="center" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/CAN-bus-frame-standard-message-SOF-ID-RTR-Control-Data-CRC-ACK-EOF.svg">

## Adressing devices 📬
The arbitration field contains 3 identifier, which determines who will be addressed. The first 4 bits mean the class of the data, the second 4 bits mean the desired device and thelast 3 bits determine the type of the message.

## Devices ➡️
## Message types: 
COMMAND `0x00`  &emsp; &emsp; &emsp; RESPONSE `0x01` &emsp; &emsp; &emsp; REFERENCE `0x02` &emsp; &emsp; &emsp;  MEASURMENT `0x03` &emsp; &emsp; &emsp;   STATUS `0x04` </br>  CONFIG `0x05` &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp;   SPECIAL MESSAGE TYPE `0x06` &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; MESSAGE TYPE EXTENSION `0x07`
  



### Power Management
- Class ID :  `0x0E`
- Device ID: `0x01`

> VSRV
- Message type :  `0x00`
> HVDC
> Power Management Status
> Power Management Measurments
### Servo
### Front Right Wheel
### Front Left Wheel
### Rear Right Wheel
### Rear Left Wheel
