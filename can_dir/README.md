# CAN protocol 📑

<img align="right" width="325" height="75" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/sztaki_logo_kek.png">

CAN is a vehicle communication protocol, which is developed by Bosch. The idea behind that framework is to realize a master-slave communication through a bus, and with adressing certain Nodes give commands or get network diagnostics. Each frame contains an arbitration field, a DLC field(Data length counter), and the data field which has to be declared if we would like to communicate. The data will be sent in hexadecimal arrays, with maximal byte length of 8. We won't use the extended data, only the standard CAN Frame length.

<img align="center" src="https://github.com/istvan-knab/jarmuiranyitas_2/blob/main/Old%20Documentation/Pictures/CAN-bus-frame-standard-message-SOF-ID-RTR-Control-Data-CRC-ACK-EOF.svg">

## Adressing devices 📬
The arbitration field contains 3 identifier, which determines who will be addressed. The first 4 bits mean the class of the data, the second 4 bits mean the desired device and thelast 3 bits determine the type of the message.

## Devices ➡️
## Message types: 

COMMAND &emsp;&ensp;`0x00` &emsp; &emsp; &emsp;&emsp;&ensp;&nbsp; STATUS &emsp; &emsp; &emsp;&emsp; &emsp; &emsp; &emsp; &ensp;  `0x04` </br>
RESPONSE &emsp;&ensp;  `0x01` &emsp; &emsp; &emsp; &emsp;&ensp; CONFIG &emsp; &emsp; &emsp;&emsp; &emsp; &emsp; &emsp; &ensp;`0x05` </br>
REFERENCE &emsp; `0x02` &emsp; &emsp; &emsp; &emsp;&ensp; SPECIAL MESSAGE TYPE &emsp; `0x06` </br>
MEASURMENT `0x03` &emsp; &emsp; &emsp;&emsp;&ensp; MESSAGE TYPE EXTENSION `0x07`



### Power Management
- Class ID :  `0x0E`
- Device ID: `0x01`

> VSRV ( Command )
- Message type :  `0x00`
- DLC : 2

|  Byte offset  |    Message    |     Data    |     Format   |
| ------------- | ------------- |-------------|--------------|
|      0        |    CMD VSRV   |    0x20     |      U8      |
|      1        |    VSRV ON    |    0x01     |      U8      |
|               |    VSRV OFF   |    0x02     |      U8      |

> HVDC ( Command )
- Message type :  `0x00`
- DLC : 2

|  Byte offset  |    Message    |     Data    |     Format   |
| ------------- | ------------- |-------------|--------------|
|      0        |    CMD HVDC   |    0x30     |      U8      |
|      1        |    HVDC ON    |    0x01     |      U8      |
|               |    HVDC OFF   |    0x02     |      U8      |
> Power Management Status
- Message type :  `0x04`
- DLC : 3

|  Byte offset  |    Message     |     Data    |     Format   |
| ------------- | -------------  |-------------|--------------|
|      0        |   Main Switch  |      -      |      BIT0    |
|               |      VSRV      |      -      |      BIT1    |
|               |   HV Charging  |      -      |      BIT2    |
|               |    HV Brake    |      -      |      BIT3    |
|        1      |LV_Battery_state|      -      |     U8       |
|        2      |HV_Battery_state|      -      |     U8       |
- HV,LV State Values : `0x00 – Ok` `0x01 – Low` `0x02 – Critical` `0x03 – Dead`

> Power Management Measurments
- Message type : `0x03`
- DLC : 8

|  Byte offset  |    Message     |     Data    |     Format   |
| ------------- | -------------  |-------------|--------------|
|      0        |   VbatLV       |      -      |      U16     |
|      2        |   VbatHV       |      -      |      U16     |
|      4        |   VDC          |      -      |      U16     |
|      6        |   Im           |      -      |      I16     |

### Servo
- Class ID :  `0x0D`
- Device ID: `0x01`

> Discover( Command )
- Message type :  `0x00`
- DLC : 2

|  Byte offset  |    Message    |     Data    |     Format   |
| ------------- | ------------- |-------------|--------------|
|      0        |  CMD Discover |    0x90     |      U8      |

> Mode( Command )
- Message type :  `0x00`
- DLC : 2

|  Byte offset  |    Message     |     Data    |     Format   |
| ------------- | -------------  |-------------|--------------|
|      0        |   CMD Mode     |    0xBB     |      U8      |
|      1        |   Mode Idle    |    0xB0     |      U8      |
|      1        |   Mode Start   |    0x0B     |      U8      |
 
### Front Right Wheel
### Front Left Wheel
### Rear Right Wheel
### Rear Left Wheel
