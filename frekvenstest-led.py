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

# Start PWM'en med en DutyCycle på 50 så den er tændt 50% af tiden.
p.start(50)


try:
	while True:
			time.sleep(0.2)

except KeyboardInterrupt:
	pass

# Stop PWM'en.
p.stop()

# Nulstil GPIO instilningerne.
GPIO.cleanup()
