# -*- encoding: latin-1 -*-
import RPi.GPIO as GPIO
import time

# Konfigurer Raspberry PI's GPIO.
# Fortæl hvilken måde hvorpå vi fortolker GPIO pin's på.
GPIO.setmode(GPIO.BOARD)

# Set pin nummer 18 til output.
GPIO.setup(18, GPIO.OUT)

# Sørg for at slukke før vi tænder.
GPIO.output(18, 0)

# Lav et nyt PWM objekt i variable p og intialiser det med en frekvens af 60 Hz.
p = GPIO.PWM(18, 60)

# Start PWM'en med en DutyCycle på 0 så den starter slukket.
p.start(100)


try:
	while True:
		# Her laver vi en løkke der gør LED'en lyser.
		for i in range(100):
			p.ChangeDutyCycle(i)
			time.sleep(0.02)
		# Her laver vi en løkke der gør LED'en mørker.
		for i in range(100):
			p.ChangeDutyCycle(100-i)
			time.sleep(0.02)

except KeyboardInterrupt:
	pass

# Stop PWM'en.
p.stop()

# Nulstil GPIO instilningerne.
GPIO.cleanup()
