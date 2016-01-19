# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Set pin nummer 11 til input.
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set pin nummer 18 til output.
GPIO.setup(18, GPIO.OUT)

# Sørg for at slukke før vi tænder.
GPIO.output(18, 0)

try:

	# Start en uendelig løkke og afbryd hvis ctrl-c bliver trykket.
	while True:
		GPIO.output(18, GPIO.input(11) == 0)

except KeyboardInterrupt:
	# Nulstil GPIO instilningerne.
	GPIO.cleanup()
