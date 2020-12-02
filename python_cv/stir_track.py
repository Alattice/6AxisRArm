import numpy as np
import cv2
from pySerialTransfer import pySerialTransfer as txfer
import time
import math

#import usb_interface
# Open the device at the ID 0
cap = cv2.VideoCapture(0)

#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
	print("Could not open video device")

width = 640
height = 480
#To set the resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height);
link = txfer.SerialTransfer('/dev/ttyUSB0', baud=115200)
link.open()
time.sleep(2) # allow some
for a in range(6):
	link.txBuff[a] = 50
	link.txBuff[2] = 20

circle_gen = False
xyr = [0,0,0]
cvxyr = [0,0,0]
angle = 100

while (True):
	ret, frame = cap.read()
	overlay = frame.copy();
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	if not circle_gen:
		circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100)

		if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
			circles = np.round(circles[0, :]).astype("int")
		# loop over the (x, y) coordinates and radius of the circles
			for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
				cv2.circle(overlay, (x, y), r, (0, 255, 0), 4)
				if (r > 0) and (x > 0) and (y > 0):
					xyr[0] = int(100-100*x/width)
					xyr[1] = int(100-100*y/height)
					xyr[2] = int(100*r/480)
					cvxyr = x,y,r
					origin = [xyr[0],xyr[1]]
					increment = 40
					rad = xyr[2]
					circle_gen = True
			
	#stir if circlei
	if circle_gen:
		try:
				ret, frame = cap.read()
				overlay = frame.copy();
				#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				#screen_stat = str("x: {} y: {} r: {}".format(xyr[0],xyr[1],xyr[2]))
				#cv2.putText(overlay,screen_stat,(5,15),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0),2,cv2.LINE_AA)
				cv2.circle(overlay, (cvxyr[0], cvxyr[1]), cvxyr[2], (0, 255, 0), 4)
				cv2.imshow("output", overlay)

				j1 = origin[0]+rad*math.cos(math.radians(angle))*math.exp(angle/(-360))
				j2 = origin[1]+rad*math.sin(math.radians(angle))+(angle/360)*3
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
			link.txBuff[0] = 50
			link.txBuff[1] = 0
			link.txBuff[2] = 0
			for a in range(3,5):
				link.txBuff[a] = 50
			link.send(6)
			time.sleep(1)
			link.close()
			cap.release()
			cv2.destroyAllWindows()

	screen_stat = str("x: {} y: {} r: {}".format(xyr[0],xyr[1],xyr[2]))
	cv2.putText(overlay,screen_stat,(5,15),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2,cv2.LINE_AA)
	cv2.imshow("output", overlay)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		link.txBuff[0] = 50
		link.txBuff[1] = 0
		link.txBuff[2] = 0
		for a in range(3,5):
			link.txBuff[a] = 50
		link.send(6)
		time.sleep(1)
		link.close()
		cap.release()
		cv2.destroyAllWindows()
		break