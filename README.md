# 6AxisRArm
install guide
For python openCV:
run sudo apt install python3-opencv
this will install all the python and opencv needed
For Arduino:
-install the SerialTransfer.h library by PowerBroker through the llibrary manager or github https://github.com/PowerBroker2/SerialTransfer
For Python:
-install Python 3.x
-Install https://github.com/PowerBroker2/pySerialTransfer through pip

The serialComm2 code will work without the openCV, simply accompany it with example codes in python_no_cv/

Both will need the arduino device defined in the code where 
link = txfer.SerialTransfer('/dev/ttyUSB0', baud=115200)
for linux, this can be found with 
ls -l /dev/ttyUSB*
This lists all arduinos attached to the usb ports. ttyUSB is the prefix for arduino nano, other models may identify itself as ttyAc*
Occasionally if the script is not run from terminal with admin permission, the following command will need to be run
sudo chmod a+rw /dev/ttyUSB*
where * is the port being used by the arduino

