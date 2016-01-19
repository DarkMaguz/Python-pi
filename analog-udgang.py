# -*- encoding: latin-1 -*-

# 
from smbus import SMBus
from time import sleep

bus = SMBus(1)
address = 74

control = 1<<6 # Aktiver analog udgang.

print("Udskriv en rampe til D/A'en")
print("Ctrl C to stop")
while True:
	for a in range(0,256):
		bus.write_byte_data(address, control, a) # Send data til D/A
		sleep(0.01)
