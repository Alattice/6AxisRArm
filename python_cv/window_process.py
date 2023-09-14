############################################
# separate thread that manages window updates
# python 3.6.9
#
############################################ 

import threading
import queue

class window_process(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def update(self): #update the window
