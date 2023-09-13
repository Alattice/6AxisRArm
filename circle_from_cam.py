import numpy as np
import cv2

#import usb_interface
# Open the device at the ID 0
cap = cv2.VideoCapture(0)

#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
	print("Could not open video device")

#To set the resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);

while(True):
# Capture frame-by-frame
	ret, frame = cap.read()
	overlay = frame.copy();
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# detect circles in the frame
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100)
# Display the resulting frame
	# ensure at least some circles were found
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv2.circle(overlay, (x, y), r, (0, 255, 0), 4)
			#cv2.rectangle(overlay, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			#cv2.rectangle(overlay, (x-r,y-r) , (x+r,y+r) , (36,48,201), 5)
		# show the output image
		screen_stat = str("x: {} y: {} r: {}".format(int(100-100*x/640),int(100-100*y/480),int(100*r/480)))
		cv2.putText(overlay,screen_stat,(5,15),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0),2,cv2.LINE_AA)
		cv2.imshow("output", overlay)

	else:
		#print("nothing detected")
		pass
	cv2.imshow("output", overlay)
#Waits for a user input to quit the application

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	#usb_interface.connection_active()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()