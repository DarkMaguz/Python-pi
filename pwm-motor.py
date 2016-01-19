# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Set pin nummer 11 til output.
GPIO.setup(11, GPIO.OUT)

# Sørg for at slukke før vi tænder.
GPIO.output(11, 0)

# Lav et nyt PWM objekt i variable p og intialiser det med en frekvens af 200 Hz.
p = GPIO.PWM(11, 500)

# Start PWM'en med en DutyCycle på 0 så den starter slukket.
p.start(0)

try:
	while True:
		# Her laver vi en løkke der gør motoren sætter farten op.
		for i in range(100):
			p.ChangeDutyCycle(i)
			time.sleep(0.03)
		# Her laver vi en løkke der gør motoren sætter farten ned.
		for i in range(100):
			p.ChangeDutyCycle(100-i)
			time.sleep(0.03)

except KeyboardInterrupt:
	pass

# Stop PWM'en.
p.stop()

# Nulstil GPIO instilningerne.
GPIO.cleanup()
