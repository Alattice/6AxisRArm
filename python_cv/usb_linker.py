##########
# Class in charge of connecting to the Arduino/ robot arm
# interface/device & sending move commands
#
#
##########

from pySerialTransfer import pySerialTransfer as txfer
from serial.tools import list_ports
import time

class usb_linker():
	def __init__(self):
		#threading.Thread.__init__(self)
		self.usb_link = None
		self.init_usb()

	def init_usb(self):
		try:
			ports = list(list_ports.comports()) #print(list_ports.grep("ttyUSB0"))
			device_port = None
			for port in ports:
				print(port)
				print(port.device)
				print(port.hwid)
				print(port.description)
				if "Arduino" in port.description or "CH340" in port.description:
					print("Arduino detected on ", port.device)
					device_port = port.device
				elif 'ttyUSB' in port.device:
					device_port = port.device
					print("no specific arduino detected but found {} on {}".format(port.description,port.device))

				self.usb_link = txfer.SerialTransfer(device_port, baud=115200)

				self.usb_link.open()
				break
		except Exception as err:
			print("Error getting usb")
			return 1

	def watchdog(self): # polls ports to ensure arduino is still connected
		pass

	def close(self):
		self.usb_link.txBuff[0] = 50
		self.usb_link.txBuff[1] = 0
		self.usb_link.txBuff[2] = 0
		for a in range(3,5):
			self.usb_link.txBuff[a] = 50
		self.usb_link.send(6)
		time.sleep(1)
		self.usb_link.close()
		return 0