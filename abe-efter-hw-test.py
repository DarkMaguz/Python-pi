# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
from time import sleep
import random

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

# Et array med de GPIO nummer der er forbundet til knapper.
knapper = [18, 23, 24, 25]
# Et array med de GPIO nummer der er forbundet til LEDs.
lamper = [4, 17, 27, 22]
# Et array med farverne i den rækkefølge de er stillet på bordet.
farver = ["rød", "grøn", "gul", "blå"]

# Set GPIO pin's i arrayet "knapper" til input.
for pin in knapper:
	GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set GPIO pin's i arrayet "lamper" til output.
for pin in lamper:
	GPIO.setup(pin, GPIO.OUT)
	#GPIO.output(pin, 0)

try:

	# Start en uendelig løkke og afbryd hvis ctrl-c bliver trykket.
	while True:
		for i in range(0, 4):
			if GPIO.input(knapper[i]) == 0:
				GPIO.output(lamper[i], 0)
			else:
				GPIO.output(lamper[i], 1)

except KeyboardInterrupt:
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()
