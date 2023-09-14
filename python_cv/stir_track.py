##################################
# main file for robot arm stirring
# takes input of webcam port
# uses webcam to monitor for a circle (pot) and identifies
# circumference path. Coordinates are sent to robot arm to 
# follow & stir pot when spoon is attached
#
#
# built on python 3.6.9
# dependencies: numpy, pySerialTransfer(python & arduino)
###################################

import numpy as np
import cv2
#from pySerialTransfer import pySerialTransfer as txfer
#from serial.tools import list_ports
import time
import math
import threading
import queue
import traceback
import sys

import usb_linker as usb
#import window_process as view

class window_process(threading.Thread):
	def __init__(self, frame_data):
		threading.Thread.__init__(self)
		self.window_W = 640
		self.window_H = 480
		self.cam_stream = None
		self.overlay = None
		self.init()
		self.window_proc = threading.Thread(target=self.update)
		self.window_proc.name = 'window_update_manager'
		self.window_proc.start()

	def init(self):
		try:
			# Open the device at the ID 0
			self.cam_stream = cv2.VideoCapture(self.vid_cap_device)
			

			#Check whether user selected camera is opened successfully.
			if not (self.cam_stream.isOpened()):
				print("Could not open video device")
				return 1

			#set window resolution
			self.cam_stream.set(cv2.CAP_PROP_FRAME_WIDTH,self.window_W);
			self.cam_stream.set(cv2.CAP_PROP_FRAME_HEIGHT,self.window_H);

		except Exception as err:
			print("error relating to video device occured: {}".format())

	def update(self): #update the window
		cv2.imshow("output", overlay)
		pass

	def close(self):
		self.window_proc.join()
		pass

#------------------------------window end-----------------
#------------------------------cv other start------------

class cv_module(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
		#cv
		self.vid_cap_device = 0 #default webcam on linux
		#self.videoStream
		# self.window_W = 640
		# self.window_H = 480
		# self.cam_stream = None


		self.user_params()
		#self.init_window()
		

		#start window thread
		#self.window = window_process.window_handler()
			
	# fetch user args from console. takes 1 video arg [-1/0/1]
	def user_params(self): #cmd args from user
		num_args = len(sys.argv)
		if num_args == 1: #no param given, assume video0
			#self.vid_cap_device = 0
			print("No user input, assuming {}".format(self.vid_cap_device))
		else:
			self.vid_cap_device = int(sys.argv[1])
			print("Using {} as video input".format(self.vid_cap_device))


	# def init_window(self):
	# 	try:
	# 		# Open the device at the ID 0
	# 		self.cam_stream = cv2.VideoCapture(self.vid_cap_device)
			

	# 		#Check whether user selected camera is opened successfully.
	# 		if not (self.cam_stream.isOpened()):
	# 			print("Could not open video device")
	# 			return 1

	# 		#set window resolution
	# 		self.cam_stream.set(cv2.CAP_PROP_FRAME_WIDTH,self.window_W);
	# 		self.cam_stream.set(cv2.CAP_PROP_FRAME_HEIGHT,self.window_H);

	# 	except Exception as err:
	# 		print("error relating to video device occured: {}".format())

	# def window_handler(self):
	# 	pass

#============================== main routine ================================
robot_arm = usb()
session = cv_module()
cam_view = view()

#set default robot joint pos
for a in range(6):
	robot_arm.usb_link.txBuff[a] = 50 #set default positions
	robot_arm.usb_link.txBuff[2] = 20 #set default position joint 2

circle_gen = False #flag for if circle is detected
xyr = [0,0,0]
cvxyr = [0,0,0]
angle = 100

while (True): #main routine
	ret, frame = session.cam_stream.read()
	cam_view.overlay = frame.copy();
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
					xyr[0] = int(100-100*x/session.window_W)
					xyr[1] = int(100-100*y/session.window_H)
					xyr[2] = int(100*r/480)
					cvxyr = x,y,r
					origin = [xyr[0],xyr[1]]
					increment = 40
					rad = xyr[2]
					circle_gen = True
			
	#stir if circlei
	if circle_gen:
		try:
				ret, frame = session.cam_stream.read()
				cam_view.overlay = frame.copy();
				#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				#screen_stat = str("x: {} y: {} r: {}".format(xyr[0],xyr[1],xyr[2]))
				#cv2.putText(cam_view.overlay,screen_stat,(5,15),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0),2,cv2.LINE_AA)
				cv2.circle(cam_view.overlay, (cvxyr[0], cvxyr[1]), cvxyr[2], (0, 255, 0), 4)
				#cv2.imshow("output", overlay)

				j1 = origin[0]+rad*math.cos(math.radians(angle))*math.exp(angle/(-360))
				j2 = origin[1]+rad*math.sin(math.radians(angle))+(angle/360)*3
				j5 = 54-7*math.sin(math.radians(angle))*math.exp(angle/(-360))


				robot_arm.usb_link.txBuff[0] = math.floor(j1)
				robot_arm.usb_link.txBuff[1] = math.floor(j2)
				robot_arm.usb_link.txBuff[4] = math.floor(j5)

				print(robot_arm.usb_link.txBuff[0],robot_arm.usb_link.txBuff[1],robot_arm.usb_link.txBuff[4])


				robot_arm.usb_link.send(6)

				angle += increment
				if(angle >= 360):
					angle = 0
					circle_gen = False

				while not robot_arm.usb_link.available():
					if robot_arm.usb_link.status < 0:
						print('ERROR: {}'.format(robot_arm.usb_link.status))

				response = [0,0,0,0,0,0]

				for index in range(robot_arm.usb_link.bytesRead):
					response[index] = int(robot_arm.usb_link.rxBuff[index])


				print(response)
				#time.sleep(rad*0.01)
		except KeyboardInterrupt or (cv2.waitKey(1) & 0xFF == ord('q')):
			robot_arm.close()
			session.cam_stream.release()
			cv2.destroyAllWindows()

	screen_stat = str("x: {} y: {} r: {}".format(xyr[0],xyr[1],xyr[2]))
	cv2.putText(cam_view.overlay,screen_stat,(5,15),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2,cv2.LINE_AA)
	#cv2.imshow("output", overlay)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		robot_arm.close()
		session.cam_stream.release()
		cv2.destroyAllWindows()
		cam_view.close()
		break
