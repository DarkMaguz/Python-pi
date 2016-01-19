# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Lav et array med numerne pin's vi bruger til input
input_pins = [29, 31, 33, 35, 37]

# Set pin's i array'et "input_pins" til input.
for i in range(5):
	GPIO.setup(input_pins[i], GPIO.IN)

try:

	# Start en uendelig løkke og afbryd hvis ctrl-c bliver trykket.
	while True:
		for i in range(5):
			if (GPIO.input(input_pins[i]) == 1):
				print "Tangent nr: " + str(i + 1) + " blev rørt."
		time.sleep(0.3)
			

except KeyboardInterrupt:
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()
