import numpy as np
import cv2
from pySerialTransfer import pySerialTransfer as txfer
import time

# Open the device at the ID 0
cap = cv2.VideoCapture(0)
port = '/dev/ttyUSB0'

#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
	print("Could not open video device")

#open usb port
link = txfer.SerialTransfer(port, baud=115200)
link.open()
time.sleep(2) # allow some time for the Arduino to completely reset

#To set the resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);

def exit_check():
	if cv2.waitKey(1) & 0xFF == ord('q'):
	# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()
		link.close()
#start circle detection until circl is returned
def circle_bound():
# Capture frame-by-frame
	pass



if __name__ == '__main__':
	bound_obtained = False

	while(True):
		while(not bound_obtained):
			ret, frame = cap.read()
			overlay = frame.copy();
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				# detect circles in the frame
			circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100)
				# ensure at least some circles were found
			if circles is not None:
					# convert the (x, y) coordinates and radius of the circles to integers
				circles = np.round(circles[0, :]).astype("int")
					# loop over the (x, y) coordinates and radius of the circles
				for (x, y, r) in circles:
						# draw the circle in the output image, then draw a rectangle
						# corresponding to the center of the circle
					cv2.circle(overlay, (x, y), r, (0, 255, 0), 4)
						# show the output image
					cv2.imshow("output", overlay)
					bound_obtained = True
				else:
					#print("nothing detected")
					pass
			cv2.imshow("output", overlay)
			exit_check()
		ret, frame = cap.read()
		overlay = frame.copy();
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		cv2.imshow("output", overlay)
		exit_check()



