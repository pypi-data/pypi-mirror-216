# IgusD1
igusD1 is a python libary to control two igus D1 control units.

It is despite in two Control Units -> motorVert and MotorHor 
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install igusD1

```bash
pip install igusD1
```

## Usage

first step is the Initialisiation:
```bash
from igusD1.initialisierung import *
from igusD1.motorVert import *
from igusD1.MotorHor import *
```
openSer opens the port to write and read Signals
```bash
openSer(COM, Baud, timeout)
```
COM is the Port from the PC normally COM3

Baud is the Baudrate: 9600

Timeout = 0
```bash
#returns the `port`
port = openSer("COM3", 9600, 0)
```

startMotors(port) write the signal to Enable the Motors
```bash
startMotors(port)
```
To use the motors you need to reference them, this happens automatically when you use the pos() methods below,
but you can reference them also manual with the ref_vertikal() to reference the vertikal motor, ref_horizontal() to reference the horizontal motor.

### MotorVert
```bash
ref_vertikal(port)
```
Per control system 3 different positions can be specified, which can be set via direct lan connection on the control unit.
To drive to the specified position these are the methods for both motors.
For information abput the igus D1 controll units an how to specify positions have a look at the [IgusD1 Manual](https://assets.ctfassets.net/oxcgtdo88e20/AQWcl1jIZGhasmYsUkMOW/54cc1412717a60cd5d4dcf19fa624257/DE_DAS_Handbuch_dryve_D1_DE_V3.0.1.pdf)
```bash
pos1_vertikal(port)

pos2_vertikal(port)

pos3_vertikal(port)
```
### MotorHor
```bash
ref_horizontal(port)
```
```bash
pos1_horizontal(port)

pos2_horizontal(port)

pos3_horizontal(port)
```
The error() function detects upcoming errors and stops both control units
```bash
error(port)
```
After an error you need to reset both control units wih the reset() method
```bash
reset(port)
```
The disable() function writes the signal to disable both motors
```bash
disable(port)
```
The closeSer() function writes the signal to close the port
```bash
closeSer(port)
```

