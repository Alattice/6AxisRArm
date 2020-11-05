import numpy as np
import cv2

# Open the device at the ID 0
cap = cv2.VideoCapture(0)

#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
	print("Could not open video device")

#To set the resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);

#start circle detection until circl is returned
def circle_bound():
	bool bound_obtained = False
	while(not bound_obtained):
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
		else:
			#print("nothing detected")
			pass

def update_frame():
	cv2.imshow("output", overlay)


if __name__ == '__main__':
	# Capture frame-by-frame
	ret, frame = cap.read()
	overlay = frame.copy();
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	circle_bound()

	update_frame()
	exit_check(False)



def exit_check(exit):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	# When everything done, release the capture
	if exit:
		cap.release()
		cv2.destroyAllWindows()