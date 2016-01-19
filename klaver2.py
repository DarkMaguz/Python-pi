# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Lav et array med numerne pin's vi bruger til input
input_pin = 11

# Set pin's i array'et "input_pins" til input.
#for i in range(5):
GPIO.setup(input_pin, GPIO.IN)

try:

	# Start en uendelig løkke og afbryd hvis ctrl-c bliver trykket.
	while True:
#		for i in range(5):
		if (GPIO.input(input_pin) == 0):
			print "Tangent nr: " + str(1) + " blev rørt."
		time.sleep(0.3)
			

except KeyboardInterrupt:
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()
