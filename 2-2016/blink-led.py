# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Set pin nummer 18 til output.
GPIO.setup(18, GPIO.OUT)

GPIO.output(18, 0)

for x in range(1,10):
	# Sørg for at slukke før vi tænder.
	# Tænd for LED.
	GPIO.output(18, 1)
	# Vent i 3 sekunder.
	time.sleep(1)
	GPIO.output(18, 0)
	time.sleep(1)

# Nulstil GPIO instilningerne.
GPIO.cleanup()
