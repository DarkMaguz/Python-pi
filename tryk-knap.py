# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Set pin nummer 7 til input med en pull up modstand.
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
	# Start en uendelig løkke og afbryd hvis ctrl-c bliver trykket.
	while True:
		if (GPIO.input(7) == 0):
			print "Knap trykket"
			time.sleep(0.3)
			

except KeyboardInterrupt:
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()
