# 6AxisRArm

6AxisRArm is a library that attempts to unify control of a 6-axis robot arm with OpenCV so that a user can skip the development of the arm movement and communication of the arm (running on an Arduino Nano) with a computer (running linux & opencv via python).


<img src="https://github.com/Alattice/6AxisRArm/blob/main/images/20201206_120231.jpg" width="600" hieght="auto">

## Install

For python(3.x) openCV:
open terminal and run

```sudo apt install python3-opencv```

```sudo apt install python3-pip```

```pip3 install pySerialTransfer```

this will install all the python and opencv needed

For Arduino:

-install the SerialTransfer.h library by PowerBroker through the llibrary manager or github https://github.com/PowerBroker2/SerialTransfer

The serialComm2 code will work without the openCV, simply accompany it with example codes in python_no_cv/

Both will need the arduino device defined in the code where 
link = txfer.SerialTransfer('/dev/ttyUSB0', baud=115200)
for linux, this can be found with

```ls -l /dev/ttyUSB*```

This lists all arduinos attached to the usb ports. ttyUSB is the prefix for arduino nano, other models may identify itself as ttyAc*

Occasionally if the script is not run from terminal with admin permission, the following command will need to be run

```sudo chmod a+rw /dev/ttyUSB*```

where * is the port being used by the arduino

[![IMAGE ALT TEXT](http://img.youtube.com/vi/cXKHj_ff0_4/0.jpg)](https://www.youtube.com/watch?v=cXKHj_ff0_4 "Robot stir test")

