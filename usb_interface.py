print("usb interface")
from pySerialTransfer import pySerialTransfer as txfer
import time

def usb_connection(link,status):
    if status==1:
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
    else:
    	link.close()

def usb_send(link, pos_list):
    for a in range(6):
        link.txBuff[a] = pos_list[a]

    link.send(6)

    while not link.available():
        if link.status < 0:
            print('ERROR: {}'.format(link.status))
   
    print('Response received:')
    response = [0,0,0,0,0,0]
    for index in range(link.bytesRead):
#    response += chr(link.rxBuff[index])
        response[index] = int(link.rxBuff[index])
    print(response)
    time.sleep(1)
