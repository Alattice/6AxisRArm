from pySerialTransfer import pySerialTransfer as txfer
import time
import math
if __name__ == '__main__':
    try:
        link = txfer.SerialTransfer('COM13', baud=115200)

        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset

        #origin:    x,y of center of the circle
        #increment: steps to increment servos
        #rad:       radius of the circle
        origin = [50,60]
        increment = 40
        rad = 20

        #initial angle 
        angle = 100

        #initial default values
        for a in range(6):
            link.txBuff[a] = 50
        link.txBuff[2] = 20

        while True:
            j1 = origin[0]+rad*math.cos(math.radians(angle))*math.exp(angle/(-360))
            j2 = origin[1]+rad*math.sin(math.radians(angle))
            j5 = 63-7*math.sin(math.radians(angle))*math.exp(angle/(-360))


            link.txBuff[0] = math.floor(j1)
            link.txBuff[1] = math.floor(j2)
            link.txBuff[4] = math.floor(j5)

            print(link.txBuff[0],link.txBuff[1],link.txBuff[4])

            link.send(6)

            angle += increment
            if(angle >= 360):
                angle = 0
       
            while not link.available():
                if link.status < 0:
                    print('ERROR: {}'.format(link.status))
       
            response = [0,0,0,0,0,0]

            for index in range(link.bytesRead):

                response[index] = int(link.rxBuff[index])

       
            print(response)
            time.sleep(rad*0.017)
       
    except KeyboardInterrupt:
        #return to initial position
        link.txBuff[0] = 50
        link.txBuff[1] = 0
        link.txBuff[2] = 0
        for a in range(3,5):
            link.txBuff[a] = 50
        link.send(6)
        time.sleep(1)
        link.close()
